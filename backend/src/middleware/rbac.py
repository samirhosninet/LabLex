from typing import List
from fastapi import Depends, status
from src.middleware.scoping import get_current_user_membership
from src.core.errors import LabLexException

class RequireRole:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: tuple = Depends(get_current_user_membership)):
        user_id, tenant_id, role = current_user
        
        # Check if user's role is in the allowed roles
        if role not in self.allowed_roles:
            raise LabLexException(
                code="FORBIDDEN",
                message=f"Access denied. Required role: one of {self.allowed_roles}.",
                status_code=status.HTTP_403_FORBIDDEN
            )
        return current_user
