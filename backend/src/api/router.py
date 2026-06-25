from fastapi import APIRouter
from src.api.health import router as health_router
from src.api.auth import router as auth_router
from src.api.registry import router as registry_router
from src.api.runspecs import router as runspecs_router
from src.api.runs import router as runs_router
from src.api.comparisons import router as comparisons_router
from src.api.audit import router as audit_router

api_router = APIRouter()

# Include routers
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(registry_router)
api_router.include_router(runspecs_router)
api_router.include_router(runs_router)
api_router.include_router(comparisons_router)
api_router.include_router(audit_router)
