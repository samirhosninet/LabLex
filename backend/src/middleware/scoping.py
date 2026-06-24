from contextvars import ContextVar
from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import hashlib
from src.core.database import get_db
from src.core.security import decode_access_token
from src.models.tenant import Membership
from src.models.api_key import APIKey
from src.core.errors import LabLexException

# Context variable to hold the current request's tenant_id
current_tenant_id: ContextVar[Optional[str]] = ContextVar("current_tenant_id", default=None)

security = HTTPBearer(auto_error=False)

def get_tenant_scoped_db(db: Session = Depends(get_db)):
    # Dependency that can be used to yield a database session that automatically
    # filters or check scoping (or we check scoping in API endpoints)
    return db

async def get_current_user_membership(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    api_key_header: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> tuple[str, str, str]: # returns (user_id/api_key_id, tenant_id, role)
    # 1. Check API Key
    if api_key_header:
        hashed_key = hashlib.sha256(api_key_header.encode()).hexdigest()
        key_record = db.query(APIKey).filter(APIKey.key_hash == hashed_key, APIKey.revoked_at == None).first()
        if not key_record:
            raise LabLexException(
                code="UNAUTHORIZED",
                message="Invalid or revoked API key.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Update last used
        key_record.last_used_at = db.query(APIKey).session.bind.execute(
            # Just inline update
        ) # We can update it later or during execution
        db.commit()

        # Set tenant context
        current_tenant_id.set(key_record.tenant_id)
        return key_record.id, key_record.tenant_id, key_record.scope

    # 2. Check JWT Token
    if credentials:
        payload = decode_access_token(credentials.credentials)
        if not payload:
            raise LabLexException(
                code="UNAUTHORIZED",
                message="Invalid or expired access token.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        if not user_id or not tenant_id:
            raise LabLexException(
                code="UNAUTHORIZED",
                message="Token payload invalid.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Check membership and get role
        membership = db.query(Membership).filter(
            Membership.user_id == user_id,
            Membership.tenant_id == tenant_id
        ).first()

        if not membership:
            raise LabLexException(
                code="FORBIDDEN",
                message="User is not a member of the requested tenant.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        current_tenant_id.set(tenant_id)
        return user_id, tenant_id, membership.role

    raise LabLexException(
        code="UNAUTHORIZED",
        message="Authentication required.",
        status_code=status.HTTP_401_UNAUTHORIZED
    )
