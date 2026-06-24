from fastapi import APIRouter
from src.api.health import router as health_router
from src.api.auth import router as auth_router

api_router = APIRouter()

# Include routers
api_router.include_router(health_router)
api_router.include_router(auth_router)
