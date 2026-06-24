from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis
from src.core.database import get_db
from src.core.config import settings

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def check_health(db: Session = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "services": {
            "database": "untested",
            "redis": "untested"
        }
    }
    
    # 1. Test database
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = f"unhealthy: {str(e)}"

    # 2. Test Redis
    try:
        r = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        r.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"

    if health_status["status"] == "degraded":
        # We can still return 200 or 503 depending on preference,
        # but let's return 200 with degraded state or 503.
        # Let's return 503 if any core service is down, following edge cases rules:
        # "If Redis or Postgres is down, the health check endpoint must report degraded status (HTTP 503 Service Unavailable)"
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )

    return health_status
