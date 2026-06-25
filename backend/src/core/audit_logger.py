import functools
import uuid
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from src.models.evaluation import AuditEvent

def log_audit_event(
    db: Session,
    tenant_id: str,
    actor_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    details: dict = None
) -> AuditEvent:
    """
    Direct helper to create and persist an audit event in the database.
    """
    event = AuditEvent(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {},
        timestamp=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    return event

def audit_action(action: str, resource_type: str):
    """
    Decorator for FastAPI routes to automatically log audit events.
    Expects 'db' (Session) and 'auth' (tuple of user_id, tenant_id, role) in kwargs,
    and returns a response dict/object where we can extract a resource ID if needed.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            db: Session = kwargs.get("db")
            auth = kwargs.get("auth")

            # Fallback to positional args if not in kwargs
            if not db:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Execute the endpoint function
            result = await func(*args, **kwargs)

            # If db and auth are present, log the audit event
            if db and auth and isinstance(auth, tuple) and len(auth) >= 2:
                user_id, tenant_id, role = auth
                
                # Try to extract resource_id from result (support dict or object)
                resource_id = "unknown"
                if isinstance(result, dict):
                    resource_id = str(result.get("id") or result.get("key") or "unknown")
                elif hasattr(result, "id"):
                    resource_id = str(result.id)
                elif hasattr(result, "key"):
                    resource_id = str(result.key)

                # Collect extra details if needed
                payload = kwargs.get("payload") or {}
                details = {"payload_keys": list(payload.keys())} if isinstance(payload, dict) else {}
                
                try:
                    log_audit_event(
                        db=db,
                        tenant_id=tenant_id,
                        actor_id=user_id,
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        details=details
                    )
                except Exception as audit_err:
                    # Do not fail request if auditing fails in background, just log
                    import logging
                    logging.getLogger("lablex.audit").error(f"Failed to write audit log: {audit_err}")

            return result
        return wrapper
    return decorator
