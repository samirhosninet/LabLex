from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.core.config import settings
from src.core.errors import (
    LabLexException,
    lablex_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from src.api.router import api_router
from src.core.seed import seed_db

app = FastAPI(
    title="LabLex AI Evaluation Control Plane API",
    description="Backend services for LabLex multi-tenant AI evaluation control plane.",
    version="1.6.3",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(LabLexException, lablex_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include core API router with /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    # Seed DB on startup for ease of local development
    seed_db()
