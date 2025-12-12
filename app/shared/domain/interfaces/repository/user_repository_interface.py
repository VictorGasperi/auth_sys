from abc import ABC, abstractmethod
from typing import List, Optional

from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user_id: str, new_email: Optional[str] = None, new_hashed_password: Optional[str] = None, new_role: Optional[ROLE] = None, new_is_active: Optional[bool] = None) -> User:
        pass
