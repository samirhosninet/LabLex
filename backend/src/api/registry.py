from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import uuid

from src.core.database import get_db
from src.middleware.scoping import get_current_user_membership
from src.core.validators import validate_manifest
from src.models.evaluation import Manifest
from src.core.errors import LabLexException

router = APIRouter()

@router.post("/manifests", status_code=status.HTTP_201_CREATED)
async def create_manifest(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    
    # Verify required base fields
    required_keys = ["kind", "id", "name", "schema_version", "manifest_version"]
    for key in required_keys:
        if key not in payload:
            raise LabLexException(
                code="VALIDATION_ERROR",
                message=f"Missing required base field '{key}' in manifest.",
                status_code=400
            )
            
    kind = payload["kind"]
    manifest_id = payload["id"]
    name = payload["name"]
    schema_version = payload["schema_version"]
    manifest_version = payload["manifest_version"]
    
    # Run JSON Schema validation
    validate_manifest(kind, payload, version="v1")
    
    # Check if duplicate manifest exists for this tenant
    existing = db.query(Manifest).filter(
        Manifest.tenant_id == tenant_id,
        Manifest.kind == kind,
        Manifest.manifest_id == manifest_id
    ).first()
    
    if existing:
        raise LabLexException(
            code="CONFLICT",
            message=f"Manifest of kind '{kind}' with id '{manifest_id}' already exists for this tenant.",
            status_code=status.HTTP_409_CONFLICT
        )
        
    db_manifest = Manifest(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        kind=kind,
        manifest_id=manifest_id,
        name=name,
        schema_version=schema_version,
        manifest_version=manifest_version,
        content=payload,
        deprecated=False
    )
    
    db.add(db_manifest)
    db.commit()
    db.refresh(db_manifest)
    
    return {
        "id": db_manifest.id,
        "manifest_id": db_manifest.manifest_id,
        "kind": db_manifest.kind,
        "name": db_manifest.name,
        "status": "registered"
    }

# Specific wrapper routes for convenience and US compliance
@router.post("/external-tools", status_code=status.HTTP_201_CREATED)
async def create_external_tool(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    payload["kind"] = "external_tool"
    return await create_manifest(payload, db, auth)

@router.post("/targets", status_code=status.HTTP_201_CREATED)
async def create_target(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    payload["kind"] = "target"
    return await create_manifest(payload, db, auth)

@router.post("/models", status_code=status.HTTP_201_CREATED)
async def create_model(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    payload["kind"] = "model"
    return await create_manifest(payload, db, auth)

@router.post("/benchmarks", status_code=status.HTTP_201_CREATED)
async def create_benchmark(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    payload["kind"] = "benchmark"
    return await create_manifest(payload, db, auth)

@router.post("/adapters", status_code=status.HTTP_201_CREATED)
async def create_adapter(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    payload["kind"] = "adapter"
    return await create_manifest(payload, db, auth)

@router.post("/result-schemas", status_code=status.HTTP_201_CREATED)
async def create_result_schema(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    payload["kind"] = "result_schema"
    return await create_manifest(payload, db, auth)

@router.post("/manifests/validate")
async def validate_manifest_dry_run(
    payload: Dict[str, Any],
    auth: tuple = Depends(get_current_user_membership)
):
    kind = payload.get("kind")
    if not kind:
        raise LabLexException(
            code="VALIDATION_ERROR",
            message="Missing required field 'kind' in manifest.",
            status_code=400
        )
    validate_manifest(kind, payload)
    return {"valid": True}

@router.get("/manifests")
async def list_manifests(
    kind: Optional[str] = None,
    include_deprecated: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    query = db.query(Manifest).filter(Manifest.tenant_id == tenant_id)
    
    if kind:
        query = query.filter(Manifest.kind == kind)
        
    if not include_deprecated:
        query = query.filter(Manifest.deprecated == False)
        
    total_count = query.count()
    manifests = query.offset(skip).limit(limit).all()
    
    return {
        "items": [
            {
                "id": m.id,
                "manifest_id": m.manifest_id,
                "kind": m.kind,
                "name": m.name,
                "schema_version": m.schema_version,
                "manifest_version": m.manifest_version,
                "deprecated": m.deprecated,
                "content": m.content,
                "created_at": m.created_at
            } for m in manifests
        ],
        "total_count": total_count,
        "skip": skip,
        "limit": limit
    }

@router.get("/manifests/{id}")
async def get_manifest(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    manifest = db.query(Manifest).filter(
        Manifest.id == id,
        Manifest.tenant_id == tenant_id
    ).first()
    
    if not manifest:
        # Fallback to search by manifest_id
        manifest = db.query(Manifest).filter(
            Manifest.manifest_id == id,
            Manifest.tenant_id == tenant_id
        ).first()
        
    if not manifest:
        raise LabLexException(
            code="NOT_FOUND",
            message="Manifest not found.",
            status_code=404
        )
        
    return manifest.content

@router.delete("/manifests/{id}")
async def delete_manifest(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    manifest = db.query(Manifest).filter(
        Manifest.id == id,
        Manifest.tenant_id == tenant_id
    ).first()
    
    if not manifest:
        # Fallback to search by manifest_id
        manifest = db.query(Manifest).filter(
            Manifest.manifest_id == id,
            Manifest.tenant_id == tenant_id
        ).first()
        
    if not manifest:
        raise LabLexException(
            code="NOT_FOUND",
            message="Manifest not found.",
            status_code=404
        )
        
    manifest.deprecated = True
    db.commit()
    return {"message": f"Manifest '{manifest.manifest_id}' of kind '{manifest.kind}' was deprecated."}
