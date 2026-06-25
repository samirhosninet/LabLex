from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import uuid
import io

from src.core.database import get_db
from src.middleware.scoping import get_current_user_membership
from src.models.evaluation import Comparison, ComparisonItem, ToolRun
from src.core.errors import LabLexException
from src.core.comparison_engine import calculate_comparison
from src.core.report import generate_comparison_report, generate_comparison_csv

from src.core.audit_logger import audit_action

router = APIRouter()

@router.post("/comparisons", status_code=status.HTTP_201_CREATED)
@audit_action("create_comparison", "comparison")
async def create_comparison(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Creates a new side-by-side comparison between two runs.
    """
    user_id, tenant_id, role = auth
    run_id_a = payload.get("run_id_a")
    run_id_b = payload.get("run_id_b")
    name = payload.get("name")

    if not run_id_a or not run_id_b:
        raise LabLexException(
            code="VALIDATION_ERROR",
            message="Both run_id_a and run_id_b are required.",
            status_code=400
        )

    # 1. Verify runs exist and belong to tenant
    run_a = db.query(ToolRun).filter(ToolRun.id == run_id_a, ToolRun.tenant_id == tenant_id).first()
    run_b = db.query(ToolRun).filter(ToolRun.id == run_id_b, ToolRun.tenant_id == tenant_id).first()

    if not run_a or not run_b:
        raise LabLexException(
            code="NOT_FOUND",
            message="One or both runs not found or access denied.",
            status_code=404
        )

    # 2. Calculate comparison (handles validation checks on completed states)
    compared = calculate_comparison(run_id_a, run_id_b, db)

    # 3. Create Comparison in DB
    comp = Comparison(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        name=name or f"Comparison: {run_id_a[:8]} vs {run_id_b[:8]}",
        metrics_delta=compared["summary"]
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)

    # Add items
    item_a = ComparisonItem(id=str(uuid.uuid4()), comparison_id=comp.id, run_id=run_id_a)
    item_b = ComparisonItem(id=str(uuid.uuid4()), comparison_id=comp.id, run_id=run_id_b)
    db.add(item_a)
    db.add(item_b)
    db.commit()

    return {
        "id": comp.id,
        "name": comp.name,
        "metrics_delta": comp.metrics_delta,
        "created_at": comp.created_at,
        "runs": [run_id_a, run_id_b]
    }

@router.get("/comparisons")
async def list_comparisons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Lists all saved comparisons for the tenant.
    """
    user_id, tenant_id, role = auth
    query = db.query(Comparison).filter(Comparison.tenant_id == tenant_id).order_by(Comparison.created_at.desc())
    total_count = query.count()
    comparisons = query.offset(skip).limit(limit).all()

    return {
        "items": [
            {
                "id": c.id,
                "name": c.name,
                "metrics_delta": c.metrics_delta,
                "created_at": c.created_at,
                "runs": [item.run_id for item in c.items]
            } for c in comparisons
        ],
        "total_count": total_count,
        "skip": skip,
        "limit": limit
    }

@router.get("/comparisons/{id}")
async def get_comparison_details(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Retrieves full side-by-side compared details including samples.
    """
    user_id, tenant_id, role = auth
    comp = db.query(Comparison).filter(Comparison.id == id, Comparison.tenant_id == tenant_id).first()
    if not comp:
        raise LabLexException(
            code="NOT_FOUND",
            message="Comparison not found.",
            status_code=404
        )

    run_ids = [item.run_id for item in comp.items]
    if len(run_ids) != 2:
        raise LabLexException(
            code="INVALID_STATE",
            message="Comparison is corrupted (does not have exactly 2 runs).",
            status_code=400
        )

    compared = calculate_comparison(run_ids[0], run_ids[1], db)
    return {
        "id": comp.id,
        "name": comp.name,
        "created_at": comp.created_at,
        "comparison_data": compared
    }

@router.get("/comparisons/{id}/report", response_class=HTMLResponse)
async def get_comparison_html_report(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Exports a beautiful comparison HTML report.
    """
    user_id, tenant_id, role = auth
    comp = db.query(Comparison).filter(Comparison.id == id, Comparison.tenant_id == tenant_id).first()
    if not comp:
        raise LabLexException(
            code="NOT_FOUND",
            message="Comparison not found.",
            status_code=404
        )

    report_html = generate_comparison_report(id, db)
    return HTMLResponse(content=report_html, status_code=200)

@router.get("/comparisons/{id}/export/csv")
async def export_comparison_csv(
    id: str,
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Exports side-by-side comparison data in CSV format.
    """
    user_id, tenant_id, role = auth
    comp = db.query(Comparison).filter(Comparison.id == id, Comparison.tenant_id == tenant_id).first()
    if not comp:
        raise LabLexException(
            code="NOT_FOUND",
            message="Comparison not found.",
            status_code=404
        )

    csv_content = generate_comparison_csv(id, db)
    
    # Stream file
    buffer = io.BytesIO(csv_content.encode("utf-8"))
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=comparison_{id}.csv"}
    )
