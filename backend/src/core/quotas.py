import time
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.cache import cache
from src.core.errors import LabLexException
from src.models.evaluation import ToolRun, RunSpec, TenantQuota

def check_concurrent_quota(tenant_id: str, db: Session):
    """
    Checks if the tenant has exceeded their maximum concurrent run limit.
    """
    quota = db.query(TenantQuota).filter(TenantQuota.tenant_id == tenant_id).first()
    max_concurrent = quota.max_concurrent_runs if quota else 5

    # Query running/queued runs from DB
    active_count = db.query(ToolRun).filter(
        ToolRun.tenant_id == tenant_id,
        ToolRun.status.in_(["queued", "running"])
    ).count()

    if active_count >= max_concurrent:
        raise LabLexException(
            code="QUOTA_EXCEEDED",
            message=f"Maximum concurrent runs limit of {max_concurrent} reached.",
            status_code=429
        )

def check_monthly_quota(tenant_id: str, db: Session):
    """
    Checks if the tenant has exceeded their monthly run limit.
    """
    quota = db.query(TenantQuota).filter(TenantQuota.tenant_id == tenant_id).first()
    max_monthly = quota.max_monthly_runs if quota else 100

    # Start of current calendar month
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)

    # Query count of runs created this month
    monthly_count = db.query(ToolRun).filter(
        ToolRun.tenant_id == tenant_id,
        ToolRun.created_at >= start_of_month
    ).count()

    if monthly_count >= max_monthly:
        raise LabLexException(
            code="QUOTA_EXCEEDED",
            message=f"Monthly run quota of {max_monthly} runs reached.",
            status_code=429
        )

def check_rate_limit(tenant_id: str, db: Session):
    """
    Enforces API rate limiting per tenant using Redis sliding window.
    Fail-open if Redis is unavailable.
    """
    client = cache.get_client()
    if not client:
        return  # Redis is down; fail-open to not block requests

    quota = db.query(TenantQuota).filter(TenantQuota.tenant_id == tenant_id).first()
    rate_limit = quota.rate_limit_per_minute if quota else 60

    key = cache.get_rate_limit_key(tenant_id, 0) # Use a sliding window set key
    sliding_key = f"lablex:rate_limit:sliding:{tenant_id}"
    now = time.time()
    one_minute_ago = now - 60.0

    try:
        # Use pipeline to ensure atomic sliding window operations
        pipe = client.pipeline()
        pipe.zremrangebyscore(sliding_key, "-inf", one_minute_ago)
        pipe.zcard(sliding_key)
        results = pipe.execute()

        current_requests = results[1]

        if current_requests >= rate_limit:
            raise LabLexException(
                code="RATE_LIMIT_EXCEEDED",
                message=f"API rate limit of {rate_limit} requests per minute exceeded.",
                status_code=429
            )

        # Add current request timestamp
        pipe = client.pipeline()
        pipe.zadd(sliding_key, {str(now): now})
        pipe.expire(sliding_key, 65)
        pipe.execute()

    except LabLexException:
        raise
    except Exception as e:
        # Log error and fail-open
        import logging
        logging.getLogger("lablex.quotas").error(f"Redis rate limiting error: {e}")

def check_duplicate_runspec_config(tenant_id: str, runspec_id: str, db: Session):
    """
    Detects if a runspec with the exact same component configuration is already running/queued.
    Raises 409 Conflict if a duplicate is found.
    """
    target_runspec = db.query(RunSpec).filter(
        RunSpec.id == runspec_id,
        RunSpec.tenant_id == tenant_id
    ).first()
    if not target_runspec:
        raise LabLexException(
            code="NOT_FOUND",
            message="RunSpec not found.",
            status_code=404
        )

    # Find active runs
    active_runs = db.query(ToolRun).filter(
        ToolRun.tenant_id == tenant_id,
        ToolRun.status.in_(["queued", "running"])
    ).all()

    for run in active_runs:
        if run.runspec and run.runspec.components == target_runspec.components:
            raise LabLexException(
                code="DUPLICATE_RUN_CONFIG",
                message=f"A run with the identical component configuration is already active (Run ID: {run.id}).",
                status_code=409
            )
