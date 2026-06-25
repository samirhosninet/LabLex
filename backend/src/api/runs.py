from fastapi import APIRouter, Depends, status, Request, Query, Header
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
from typing import Dict, Any, Optional
import uuid
import json
import redis
import asyncio
from datetime import datetime

from src.core.database import get_db, SessionLocal
from src.middleware.scoping import get_current_user_membership
from src.models.evaluation import ToolRun, RunSpec, NormalizedResult
from src.core.errors import LabLexException
from src.core.config import settings

from src.core.idempotency import idempotent_endpoint
from src.core.quotas import check_concurrent_quota, check_monthly_quota, check_duplicate_runspec_config
from src.core.audit_logger import audit_action

router = APIRouter()

try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception as e:
    redis_client = None

@router.post("/runs", status_code=status.HTTP_201_CREATED)
@idempotent_endpoint()
@audit_action("trigger_run", "run")
async def trigger_run(
    payload: Dict[str, Any],
    request: Request,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    runspec_id = payload.get("runspec_id")
    
    if not runspec_id:
        raise LabLexException(
            code="VALIDATION_ERROR",
            message="Missing required field 'runspec_id'.",
            status_code=400
        )
        
    runspec = db.query(RunSpec).filter(
        RunSpec.id == runspec_id,
        RunSpec.tenant_id == tenant_id
    ).first()
    
    if not runspec:
        raise LabLexException(
            code="NOT_FOUND",
            message="RunSpec not found.",
            status_code=404
        )
        
    if runspec.status != "locked":
        raise LabLexException(
            code="INVALID_STATE",
            message="Cannot run evaluation on an unlocked RunSpec. Validate and lock first.",
            status_code=400
        )

    # Quota and duplicate checks
    check_concurrent_quota(tenant_id, db)
    check_monthly_quota(tenant_id, db)
    check_duplicate_runspec_config(tenant_id, runspec_id, db)
        
    run = ToolRun(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        runspec_id=runspec_id,
        batch_id=payload.get("batch_id"),
        status="queued"
    )
    
    db.add(run)
    db.commit()
    db.refresh(run)
    
    # Trigger Celery background task
    from src.core.tasks import run_evaluation_task, publish_progress
    run_evaluation_task.delay(run.id)
    
    # Publish initial queued event
    publish_progress(run.id, "queued", 0, "Run enqueued for background worker.", {})
    
    return {
        "id": run.id,
        "runspec_id": run.runspec_id,
        "status": run.status,
        "created_at": run.created_at
    }

@router.get("/runs")
async def list_runs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    query = db.query(ToolRun).filter(ToolRun.tenant_id == tenant_id).order_by(ToolRun.created_at.desc())
    total_count = query.count()
    runs = query.offset(skip).limit(limit).all()
    return {
        "items": [
            {
                "id": r.id,
                "runspec_id": r.runspec_id,
                "status": r.status,
                "created_at": r.created_at,
                "updated_at": r.updated_at
            } for r in runs
        ],
        "total_count": total_count,
        "skip": skip,
        "limit": limit
    }

@router.get("/runs/{id}")
async def get_run_status(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    run = db.query(ToolRun).filter(
        ToolRun.id == id,
        ToolRun.tenant_id == tenant_id
    ).first()
    
    if not run:
        raise LabLexException(
            code="NOT_FOUND",
            message="Evaluation run not found.",
            status_code=404
        )
        
    return {
        "id": run.id,
        "runspec_id": run.runspec_id,
        "status": run.status,
        "error_message": run.error_message,
        "created_at": run.created_at,
        "updated_at": run.updated_at
    }

@router.get("/runs/{id}/results")
async def get_run_results(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    run = db.query(ToolRun).filter(
        ToolRun.id == id,
        ToolRun.tenant_id == tenant_id
    ).first()
    
    if not run:
        raise LabLexException(
            code="NOT_FOUND",
            message="Evaluation run not found.",
            status_code=404
        )
        
    raw_res = run.raw_results[0] if run.raw_results else None
    norm_res = run.normalized_results[0] if run.normalized_results else None
    
    samples_list = []
    if norm_res:
        samples_list = [
            {
                "sample_id": s.sample_id,
                "input_text": s.input_text,
                "expected_output": s.expected_output,
                "output_text": s.output_text,
                "error_message": s.error_message,
                "metrics": s.metrics,
                "latency_ms": s.latency_ms,
                "status": s.status
            } for s in norm_res.samples
        ]
        
    return {
        "run_id": run.id,
        "status": run.status,
        "raw_result": {
            "id": raw_res.id,
            "storage_path": raw_res.storage_path,
            "source_type": raw_res.source_type
        } if raw_res else None,
        "normalized_result": {
            "id": norm_res.id,
            "normalization_status": norm_res.normalization_status,
            "warnings": norm_res.warnings,
            "metrics_summary": norm_res.metrics_summary,
            "samples": samples_list
        } if norm_res else None
    }

# Event Generator for Server-Sent Events (SSE)
async def sse_event_generator(run_id: str, request: Request, last_event_id: Optional[str] = None, db: Optional[Session] = None):
    """
    Subscribes to Redis Pub/Sub events for the specific run_id and yields SSE events,
    with database-backed event replay and heartbeats.
    """
    import time
    from src.models.evaluation import RunEvent

    # 1. Replay missed events from database if client disconnected/reconnected
    local_db = db or SessionLocal()
    try:
        events = local_db.query(RunEvent).filter(RunEvent.run_id == run_id).order_by(RunEvent.created_at.asc()).all()
        
        events_to_replay = events
        if last_event_id:
            found_idx = -1
            for idx, ev in enumerate(events):
                if ev.id == last_event_id:
                    found_idx = idx
                    break
            if found_idx != -1:
                events_to_replay = events[found_idx + 1:]
        
        for ev in events_to_replay:
            yield {
                "event": ev.event_type,
                "id": ev.id,
                "data": json.dumps(ev.data)
            }
    except Exception as e:
        import logging
        logging.getLogger("lablex.runs").error(f"Error replaying SSE events: {e}")
    finally:
        if not db:
            local_db.close()

    # 2. Check if run is already completed. If so, terminate immediately.
    local_db = db or SessionLocal()
    try:
        run = local_db.query(ToolRun).filter(ToolRun.id == run_id).first()
        if run and run.status in ("completed", "failed", "normalization_failed"):
            return
    finally:
        if not db:
            local_db.close()

    # 3. Subscribe to Redis for live progress updates
    if not redis_client:
        yield {
            "event": "message",
            "data": json.dumps({"error": "Redis pub/sub is unavailable."})
        }
        return
        
    pubsub = redis_client.pubsub()
    channel = f"run_events:{run_id}"
    pubsub.subscribe(channel)
    
    last_heartbeat = time.time()
    
    try:
        while True:
            # Check client disconnect
            if await request.is_disconnected():
                break
                
            # Send heartbeat every 15 seconds
            now = time.time()
            if now - last_heartbeat >= 15.0:
                yield {
                    "event": "ping",
                    "data": json.dumps({"heartbeat": True, "timestamp": datetime.utcnow().isoformat()})
                }
                last_heartbeat = now

            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                data = message["data"]
                event_id = None
                try:
                    payload = json.loads(data)
                    event_id = payload.get("event_id")
                except Exception:
                    pass

                yield {
                    "event": "message",
                    "id": event_id,
                    "data": data
                }
                
                # If event signals terminal state, close generator
                try:
                    payload = json.loads(data)
                    if payload.get("status") in ("completed", "failed", "normalization_failed"):
                        break
                except Exception:
                    pass
            else:
                await asyncio.sleep(0.2)
    except Exception as e:
        yield {
            "event": "message",
            "data": json.dumps({"error": f"SSE stream error: {str(e)}"})
        }
    finally:
        try:
            pubsub.unsubscribe(channel)
        except Exception:
            pass

@router.get("/runs/{id}/events")
async def run_events_stream(
    id: str,
    request: Request,
    last_event_id: Optional[str] = Header(None, alias="Last-Event-ID")
):
    """
    Exposes an SSE stream at /api/v1/runs/{id}/events for real-time progress updates.
    Supports reconnection event replay via Last-Event-ID.
    """
    if not last_event_id:
        last_event_id = request.query_params.get("last_event_id") or request.query_params.get("Last-Event-ID")
    return EventSourceResponse(sse_event_generator(id, request, last_event_id))


@router.post("/runs/batch", status_code=status.HTTP_201_CREATED)
@audit_action("trigger_batch_runs", "batch")
async def trigger_batch_runs(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Trigger multiple evaluation runs in batch.
    """
    user_id, tenant_id, role = auth
    runspec_ids = payload.get("runspec_ids")
    max_parallel = payload.get("max_parallel", 3)

    if not runspec_ids or not isinstance(runspec_ids, list):
        raise LabLexException(
            code="VALIDATION_ERROR",
            message="Missing or invalid field 'runspec_ids'. Must be a non-empty list.",
            status_code=400
        )

    # 1. Verify all RunSpecs exist and are locked
    runspecs = db.query(RunSpec).filter(
        RunSpec.id.in_(runspec_ids),
        RunSpec.tenant_id == tenant_id
    ).all()

    if len(runspecs) != len(runspec_ids):
        raise LabLexException(
            code="NOT_FOUND",
            message="One or more RunSpecs not found.",
            status_code=404
        )

    for rspec in runspecs:
        if rspec.status != "locked":
            raise LabLexException(
                code="INVALID_STATE",
                message=f"RunSpec {rspec.id} is not locked. All RunSpecs in a batch must be locked.",
                status_code=400
            )

    # 2. Check quota limit
    # We call these to raise 429 if the tenant is already over quota
    check_concurrent_quota(tenant_id, db)
    check_monthly_quota(tenant_id, db)

    # 3. Create Batch record
    from src.models.evaluation import Batch
    batch = Batch(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        status="pending",
        total_runs=len(runspec_ids),
        max_parallel=max_parallel,
        created_by=user_id
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)

    # 4. Create and enqueue ToolRuns
    runs_data = []
    from src.core.tasks import run_evaluation_task, publish_progress
    for runspec_id in runspec_ids:
        run = ToolRun(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            runspec_id=runspec_id,
            batch_id=batch.id,
            status="queued"
        )
        db.add(run)
        db.commit()
        db.refresh(run)

        # Trigger background task
        run_evaluation_task.delay(run.id)
        publish_progress(run.id, "queued", 0, "Run enqueued as part of batch.", {})

        runs_data.append({
            "id": run.id,
            "runspec_id": run.runspec_id,
            "status": run.status,
            "created_at": run.created_at
        })

    # Transition batch status to running
    batch.status = "running"
    db.commit()

    return {
        "id": batch.id,
        "status": batch.status,
        "total_runs": batch.total_runs,
        "max_parallel": batch.max_parallel,
        "created_at": batch.created_at,
        "runs": runs_data
    }


@router.get("/runs/batches/{id}")
async def get_batch_status(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Retrieve status and progress of a batch execution.
    """
    user_id, tenant_id, role = auth
    from src.models.evaluation import Batch
    batch = db.query(Batch).filter(
        Batch.id == id,
        Batch.tenant_id == tenant_id
    ).first()

    if not batch:
        raise LabLexException(
            code="NOT_FOUND",
            message="Batch not found.",
            status_code=404
        )

    return {
        "id": batch.id,
        "status": batch.status,
        "total_runs": batch.total_runs,
        "completed_runs": batch.completed_runs,
        "failed_runs": batch.failed_runs,
        "max_parallel": batch.max_parallel,
        "created_at": batch.created_at,
        "updated_at": batch.updated_at,
        "runs": [
            {
                "id": r.id,
                "runspec_id": r.runspec_id,
                "status": r.status,
                "created_at": r.created_at
            } for r in batch.tool_runs
        ]
    }


from fastapi.responses import HTMLResponse
from src.core.report import generate_run_report

@router.get("/runs/{id}/report", response_class=HTMLResponse)
async def get_run_html_report(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    # Verify run exists and belongs to tenant
    run = db.query(ToolRun).filter(
        ToolRun.id == id,
        ToolRun.tenant_id == tenant_id
    ).first()
    
    if not run:
        raise LabLexException(
            code="NOT_FOUND",
            message="Evaluation run not found.",
            status_code=404
        )
        
    report_html = generate_run_report(id, db)
    return HTMLResponse(content=report_html, status_code=200)


from fastapi.responses import StreamingResponse
import io
from src.core.report import generate_run_csv

@router.get("/runs/{id}/export/csv")
async def export_run_csv(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Exports a completed run's normalized results in CSV format.
    """
    user_id, tenant_id, role = auth
    run = db.query(ToolRun).filter(
        ToolRun.id == id,
        ToolRun.tenant_id == tenant_id
    ).first()
    
    if not run:
        raise LabLexException(
            code="NOT_FOUND",
            message="Evaluation run not found.",
            status_code=404
        )
        
    csv_content = generate_run_csv(id, db)
    if not csv_content:
        raise LabLexException(
            code="INVALID_STATE",
            message="Run has no normalized results to export.",
            status_code=400
        )
        
    buffer = io.BytesIO(csv_content.encode("utf-8"))
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=run_{id}.csv"}
    )


@router.get("/runs/quota")
async def get_tenant_run_quota(
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Retrieves the tenant's execution quota usage.
    """
    user_id, tenant_id, role = auth
    from src.models.evaluation import TenantQuota
    quota = db.query(TenantQuota).filter(TenantQuota.tenant_id == tenant_id).first()
    
    max_concurrent = quota.max_concurrent_runs if quota else 5
    max_monthly = quota.max_monthly_runs if quota else 100
    
    # Active runs count
    active_count = db.query(ToolRun).filter(
        ToolRun.tenant_id == tenant_id,
        ToolRun.status.in_(["queued", "running"])
    ).count()
    
    # Monthly runs count
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)
    monthly_count = db.query(ToolRun).filter(
        ToolRun.tenant_id == tenant_id,
        ToolRun.created_at >= start_of_month
    ).count()
    
    return {
        "max_concurrent_runs": max_concurrent,
        "current_concurrent_runs": active_count,
        "max_monthly_runs": max_monthly,
        "current_monthly_runs": monthly_count,
        "rate_limit_per_minute": quota.rate_limit_per_minute if quota else 60
    }
