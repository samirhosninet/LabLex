from fastapi import APIRouter, Depends, status, Request, Query
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

router = APIRouter()

try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception as e:
    redis_client = None

@router.post("/runs", status_code=status.HTTP_201_CREATED)
async def trigger_run(
    payload: Dict[str, Any],
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
async def sse_event_generator(run_id: str, request: Request):
    """
    Subscribes to Redis Pub/Sub events for the specific run_id and yields SSE events.
    """
    if not redis_client:
        yield {
            "event": "message",
            "data": json.dumps({"error": "Redis pub/sub is unavailable."})
        }
        return
        
    # Check current status in DB first (if already completed, send immediately)
    db = SessionLocal()
    try:
        run = db.query(ToolRun).filter(ToolRun.id == run_id).first()
        if run and run.status in ("completed", "failed", "normalization_failed"):
            summary = {}
            if run.status == "completed" and run.normalized_results:
                summary = run.normalized_results[0].metrics_summary
            yield {
                "event": "message",
                "data": json.dumps({
                    "run_id": run_id,
                    "status": run.status,
                    "progress": 100,
                    "message": "Run already completed.",
                    "metrics_preview": summary,
                    "timestamp": datetime.utcnow().isoformat()
                })
            }
            return
    finally:
        db.close()
        
    # Subscribe to channel
    pubsub = redis_client.pubsub()
    channel = f"run_events:{run_id}"
    pubsub.subscribe(channel)
    
    try:
        while True:
            # Check client disconnect
            if await request.is_disconnected():
                break
                
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                data = message["data"]
                yield {
                    "event": "message",
                    "data": data
                }
                
                # If event signals terminal state, close generator
                try:
                    payload = json.loads(data)
                    if payload.get("status") in ("completed", "failed", "normalization_failed"):
                        break
                except Exception:
                    pass
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
async def run_events_stream(id: str, request: Request):
    """
    Exposes an SSE stream at /api/v1/runs/{id}/events for real-time progress updates.
    """
    return EventSourceResponse(sse_event_generator(id, request))


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
