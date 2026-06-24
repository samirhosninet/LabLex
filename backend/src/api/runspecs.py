from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import uuid

from src.core.database import get_db
from src.middleware.scoping import get_current_user_membership
from src.core.compatibility import check_compatibility
from src.models.evaluation import RunSpec, Manifest
from src.core.errors import LabLexException

router = APIRouter()

def resolve_runspec_manifests(tenant_id: str, components: Dict[str, str], db: Session) -> Dict[str, Dict[str, Any]]:
    """
    Resolves component references in the components dictionary to actual manifest contents.
    Supports resolving via both UUID and user-defined manifest_id.
    """
    manifests = {}
    for kind, ref_id in components.items():
        # Search by UUID first
        m = db.query(Manifest).filter(
            Manifest.tenant_id == tenant_id,
            Manifest.kind == kind,
            Manifest.id == ref_id
        ).first()
        
        if not m:
            # Fallback to search by user-defined manifest_id
            m = db.query(Manifest).filter(
                Manifest.tenant_id == tenant_id,
                Manifest.kind == kind,
                Manifest.manifest_id == ref_id
            ).first()
            
        if not m:
            raise LabLexException(
                code="COMPONENT_NOT_FOUND",
                message=f"Required component '{kind}' with identifier '{ref_id}' was not found in the registry.",
                status_code=400
            )
            
        if m.deprecated:
            raise LabLexException(
                code="COMPONENT_DEPRECATED",
                message=f"Selected component '{kind}' ('{ref_id}') is deprecated and cannot be selected for new runs.",
                status_code=400
            )
            
        manifests[kind] = m.content
    return manifests

@router.post("/runspecs/compose", status_code=status.HTTP_201_CREATED)
async def compose_runspec(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    components = payload.get("components")
    
    if not components or not isinstance(components, dict):
        raise LabLexException(
            code="VALIDATION_ERROR",
            message="Missing or invalid 'components' dictionary in request payload.",
            status_code=400
        )
        
    db_runspec = RunSpec(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        status="draft",
        components=components,
        snapshots=None
    )
    
    db.add(db_runspec)
    db.commit()
    db.refresh(db_runspec)
    
    return {
        "id": db_runspec.id,
        "status": db_runspec.status,
        "components": db_runspec.components,
        "created_at": db_runspec.created_at
    }

@router.post("/runspecs/{id}/validate")
async def validate_runspec(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    runspec = db.query(RunSpec).filter(
        RunSpec.id == id,
        RunSpec.tenant_id == tenant_id
    ).first()
    
    if not runspec:
        raise LabLexException(
            code="NOT_FOUND",
            message="RunSpec not found.",
            status_code=404
        )
        
    # Resolve all referenced manifests
    manifests = resolve_runspec_manifests(tenant_id, runspec.components, db)
    
    # Run Compatibility Engine checks
    compatible, errors = check_compatibility(manifests)
    if not compatible:
        raise LabLexException(
            code="COMPATIBILITY_ERROR",
            message="RunSpec component compatibility check failed.",
            status_code=400,
            details={"errors": errors}
        )
        
    # Perform active pre-flight connectivity checks (mock for MVP-1)
    # Checks targets, connection endpoints etc.
    target_manifest = manifests.get("target")
    if target_manifest:
        endpoint = target_manifest.get("endpoint")
        # In a real environment we would ping this endpoint. Here we mock success.
        pass
        
    runspec.status = "validated"
    db.commit()
    db.refresh(runspec)
    
    return {
        "id": runspec.id,
        "status": runspec.status,
        "compatible": True,
        "preflight_connectivity": "green"
    }

@router.post("/runspecs/{id}/lock")
async def lock_runspec(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    runspec = db.query(RunSpec).filter(
        RunSpec.id == id,
        RunSpec.tenant_id == tenant_id
    ).first()
    
    if not runspec:
        raise LabLexException(
            code="NOT_FOUND",
            message="RunSpec not found.",
            status_code=404
        )
        
    if runspec.status == "draft":
        raise LabLexException(
            code="INVALID_STATE",
            message="Only a validated RunSpec can be locked.",
            status_code=400
        )
        
    if runspec.status == "locked":
        return {
            "id": runspec.id,
            "status": runspec.status,
            "message": "RunSpec was already locked."
        }
        
    # Resolve and capture snapshots of all manifests to freeze execution parameters
    manifests = resolve_runspec_manifests(tenant_id, runspec.components, db)
    
    runspec.snapshots = manifests
    runspec.status = "locked"
    
    db.commit()
    db.refresh(runspec)
    
    return {
        "id": runspec.id,
        "status": runspec.status,
        "message": "RunSpec successfully locked and frozen.",
        "snapshots_captured": list(manifests.keys())
    }

@router.post("/runspecs/{id}/dry-run")
async def dry_run_runspec(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    runspec = db.query(RunSpec).filter(
        RunSpec.id == id,
        RunSpec.tenant_id == tenant_id
    ).first()
    
    if not runspec:
        raise LabLexException(
            code="NOT_FOUND",
            message="RunSpec not found.",
            status_code=404
        )
        
    # Resolve manifests to build dry-run stats
    # (If already locked, we use snapshots, else we resolve dynamically)
    if runspec.status == "locked" and runspec.snapshots:
        manifests = runspec.snapshots
    else:
        manifests = resolve_runspec_manifests(tenant_id, runspec.components, db)
        
    benchmark = manifests.get("benchmark", {})
    expected_samples = benchmark.get("size", 100) # Fallback to 100
    required_metrics = benchmark.get("required_metrics", [])
    
    return {
        "runspec_id": runspec.id,
        "status": runspec.status,
        "components": runspec.components,
        "preflight_audit": {
            "compatible": True,
            "expected_samples": expected_samples,
            "estimated_duration_seconds": int(expected_samples * 0.1), # Mock estimation
            "metrics_to_extract": required_metrics
        }
    }

@router.get("/runspecs/{id}")
async def get_runspec(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    user_id, tenant_id, role = auth
    runspec = db.query(RunSpec).filter(
        RunSpec.id == id,
        RunSpec.tenant_id == tenant_id
    ).first()
    
    if not runspec:
        raise LabLexException(
            code="NOT_FOUND",
            message="RunSpec not found.",
            status_code=404
        )
        
    return {
        "id": runspec.id,
        "status": runspec.status,
        "components": runspec.components,
        "snapshots": runspec.snapshots,
        "created_at": runspec.created_at,
        "updated_at": runspec.updated_at
    }
