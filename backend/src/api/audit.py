from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.core.database import get_db
from src.middleware.scoping import get_current_user_membership
from src.models.evaluation import AuditEvent

router = APIRouter()

@router.get("/audit-logs")
async def list_audit_logs(
    resource_type: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    actor_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    auth: tuple = Depends(get_current_user_membership)
):
    """
    Retrieves the audit log history for the tenant.
    """
    user_id, tenant_id, role = auth
    query = db.query(AuditEvent).filter(AuditEvent.tenant_id == tenant_id)

    if resource_type:
        query = query.filter(AuditEvent.resource_type == resource_type)
    if action:
        query = query.filter(AuditEvent.action == action)
    if actor_id:
        query = query.filter(AuditEvent.actor_id == actor_id)

    query = query.order_by(AuditEvent.timestamp.desc())
    total_count = query.count()
    events = query.offset(skip).limit(limit).all()

    return {
        "items": [
            {
                "id": ev.id,
                "actor_id": ev.actor_id,
                "action": ev.action,
                "resource_type": ev.resource_type,
                "resource_id": ev.resource_id,
                "details": ev.details,
                "timestamp": ev.timestamp
            } for ev in events
        ],
        "total_count": total_count,
        "skip": skip,
        "limit": limit
    }
