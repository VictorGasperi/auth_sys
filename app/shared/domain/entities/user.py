from pydantic import BaseModel
from app.shared.domain.enums.role import ROLE

class User(BaseModel):
    id: str
    email: str
    hashed_password: str
    role: ROLE
    is_active: bool = True
    created_at_ms: int

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at_ms": self.created_at_ms
        }
