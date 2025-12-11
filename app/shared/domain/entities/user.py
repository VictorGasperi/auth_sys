from pydantic import BaseModel

from app.shared.domain.enums.role import ROLE

class User(BaseModel):
    id: str
    email: str
    hashed_password: str
    role: ROLE
    is_active: bool = True
    created_at_ms: int


def new(
    id: str,
    email: str,
    hashed_password: str,
    role: ROLE,
    is_active: bool,
    now_ms: int
) -> "User":
    return User(
        id=id,
        email=email,
        hashed_password=hashed_password,
        role=role,
        is_active=is_active,
        created_at_ms=now_ms
    )