from typing import Optional
from pydantic import BaseModel

class AuthSession(BaseModel):
    id: str
    user_id: str
    created_at_ms: int
    expires_at_ms: int
    is_revoked: bool = False
    revoked_at_ms: Optional[int] = None
    replaced_by_session_id: Optional[str] = None

def new(
    id: str,
    user_id: str,
    created_at_ms: int,
    expires_at_ms: int
) -> "AuthSession":
    return AuthSession(
        id=id,
        user_id=user_id,
        created_at_ms=created_at_ms,
        expires_at_ms=expires_at_ms
    )