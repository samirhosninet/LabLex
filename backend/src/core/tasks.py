import json
import os
import logging
import importlib
import redis
import boto3
import uuid
from botocore.client import Config
from datetime import datetime

from src.core.celery_app import celery_app
from src.core.config import settings
from src.core.database import SessionLocal
from src.core.normalizer import normalize_result_data
from src.models.evaluation import ToolRun, RawResult, NormalizedResult, NormalizedSample

logger = logging.getLogger(__name__)

# Redis Client for Pub/Sub progress events
try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception as e:
    redis_client = None
    logger.warning(f"Could not connect to Redis for pub/sub: {e}")

def publish_progress(run_id: str, status: str, progress_percentage: int, message: str, metrics_preview: dict = None):
    """
    Publishes real-time progress events to a Redis Pub/Sub channel.
    """
    if not redis_client:
        return
    payload = {
        "run_id": run_id,
        "status": status,
        "progress": progress_percentage,
        "message": message,
        "metrics_preview": metrics_preview or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        redis_client.publish(f"run_events:{run_id}", json.dumps(payload))
    except Exception as e:
        logger.error(f"Error publishing Redis event: {e}")

def upload_raw_to_minio(tenant_id: str, run_id: str, content: dict) -> str:
    """
    Uploads raw adapter outputs to MinIO.
    Falls back to local file storage if MinIO is offline.
    """
    bucket = settings.MINIO_BUCKET_NAME
    key = f"{tenant_id}/runs/{run_id}/raw_result.json"
    content_str = json.dumps(content, indent=2)
    
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1"
        )
        # Ensure bucket exists
        try:
            s3.head_bucket(Bucket=bucket)
        except Exception:
            s3.create_bucket(Bucket=bucket)
            
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=content_str,
            ContentType="application/json"
        )
        return f"minio://{bucket}/{key}"
    except Exception as e:
        logger.warning(f"MinIO storage failed, falling back to local file system. Error: {e}")
        # Local fallback directory inside workspace
        fallback_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "temp_storage", tenant_id))
        os.makedirs(fallback_dir, exist_ok=True)
        fallback_path = os.path.join(fallback_dir, f"{run_id}_raw.json")
        with open(fallback_path, "w", encoding="utf-8") as f:
            f.write(content_str)
        return f"local://{fallback_path}"

def load_adapter_class(class_path: str):
    """
    Dynamically imports and instantiates the adapter class from class_path.
    """
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)()

@celery_app.task(name="src.core.tasks.run_evaluation_task")
def run_evaluation_task(run_id: str):
    """
    Background worker task running the evaluation workflow.
    """
    db = SessionLocal()
    try:
        run = db.query(ToolRun).filter(ToolRun.id == run_id).first()
        if not run:
            logger.error(f"ToolRun with ID {run_id} not found in database.")
            return
            
        runspec = run.runspec
        if not runspec or runspec.status != "locked":
            run.status = "failed"
            run.error_message = "Associated RunSpec is not locked."
            db.commit()
            return
            
        # 1. Start execution
        run.status = "running"
        db.commit()
        
        publish_progress(run_id, "running", 10, "Initializing adapter execution...", {})
        
        # 2. Get frozen snapshots from locked RunSpec
        snapshots = runspec.snapshots or {}
        adapter_snapshot = snapshots.get("adapter")
        target_snapshot = snapshots.get("target")
        result_schema_snapshot = snapshots.get("result_schema")
        
        if not adapter_snapshot or not result_schema_snapshot:
            run.status = "failed"
            run.error_message = "Missing adapter or result_schema snapshot in locked RunSpec."
            db.commit()
            publish_progress(run_id, "failed", 100, run.error_message, {})
            return
            
        class_path = adapter_snapshot.get("class_path")
        
        publish_progress(run_id, "running", 30, f"Loading adapter: {adapter_snapshot.get('name')}...", {})
        
        # 3. Instantiate and run adapter
        try:
            adapter = load_adapter_class(class_path)
            publish_progress(run_id, "running", 50, "Executing adapter processes...", {})
            
            # Execute adapter (runs MockAdapter which simulates predictions)
            raw_output = adapter.execute(
                runspec_snapshot={"components": runspec.components, "snapshots": snapshots},
                target_snapshot=target_snapshot or {}
            )
            
        except Exception as e:
            run.status = "failed"
            run.error_message = f"Adapter execution failed: {str(e)}"
            db.commit()
            publish_progress(run_id, "failed", 100, run.error_message, {})
            return
            
        # 4. Upload raw outputs to MinIO (or fallback)
        publish_progress(run_id, "running", 70, "Capturing and saving raw outputs...", {})
        storage_path = upload_raw_to_minio(run.tenant_id, run_id, raw_output)
        
        # Save RawResult record
        raw_res = RawResult(
            id=str(uuid.uuid4()) if hasattr(uuid, "uuid4") else os.urandom(16).hex(),
            tenant_id=run.tenant_id,
            run_id=run_id,
            storage_path=storage_path,
            storage_status="active",
            source_type="adapter"
        )
        db.add(raw_res)
        db.commit()
        db.refresh(raw_res)
        
        # 5. Normalization using JSONPath rules
        publish_progress(run_id, "running", 85, "Normalizing raw outputs into metrics...", {})
        try:
            normalized_samples, metrics_summary = normalize_result_data(raw_output, result_schema_snapshot)
            
            # Save NormalizedResult record
            norm_res = NormalizedResult(
                tenant_id=run.tenant_id,
                run_id=run_id,
                raw_result_id=raw_res.id,
                normalization_status="completed",
                warnings=[],
                metrics_summary=metrics_summary
            )
            db.add(norm_res)
            db.commit()
            db.refresh(norm_res)
            
            # Save NormalizedSample records
            for sample in normalized_samples:
                db_sample = NormalizedSample(
                    tenant_id=run.tenant_id,
                    normalized_result_id=norm_res.id,
                    sample_id=sample["sample_id"],
                    input_text=sample["input_text"],
                    expected_output=sample["expected_output"],
                    output_text=sample["output_text"],
                    error_message=sample["error_message"],
                    raw_sample_ref=sample["raw_sample_ref"],
                    metrics=sample["metrics"],
                    status=sample["status"],
                    latency_ms=sample["latency_ms"],
                    sample_metadata=sample.get("metadata")
                )
                db.add(db_sample)
                
            run.status = "completed"
            db.commit()
            
            publish_progress(run_id, "completed", 100, "Run completed successfully.", metrics_summary)
            
        except Exception as norm_err:
            run.status = "normalization_failed"
            run.error_message = f"Normalization failed: {str(norm_err)}"
            db.commit()
            
            # Save failing NormalizedResult record
            norm_res = NormalizedResult(
                tenant_id=run.tenant_id,
                run_id=run_id,
                raw_result_id=raw_res.id,
                normalization_status="failed",
                warnings=[str(norm_err)],
                metrics_summary={}
            )
            db.add(norm_res)
            db.commit()
            
            publish_progress(run_id, "normalization_failed", 100, run.error_message, {})
            
    except Exception as general_err:
        logger.error(f"General error in evaluation Celery task: {general_err}")
        try:
            run.status = "failed"
            run.error_message = f"Internal execution system error: {str(general_err)}"
            db.commit()
            publish_progress(run_id, "failed", 100, run.error_message, {})
        except Exception:
            pass
    finally:
        db.close()
