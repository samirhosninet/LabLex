from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from src.core.database import get_db
from src.core.security import verify_password, create_access_token
from src.models.user import User
from src.models.tenant import Membership
from src.core.errors import LabLexException

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tenant_id: str
    role: str

@router.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise LabLexException(
            code="INVALID_CREDENTIALS",
            message="Incorrect email or password.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get user's first membership for tenant context in MVP-0
    membership = db.query(Membership).filter(Membership.user_id == user.id).first()
    if not membership:
        raise LabLexException(
            code="NO_TENANT_MEMBERSHIP",
            message="User is not assigned to any tenant workspace.",
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    access_token = create_access_token(
        data={
            "sub": user.id,
            "tenant_id": membership.tenant_id,
            "role": membership.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tenant_id": membership.tenant_id,
        "role": membership.role
    }
