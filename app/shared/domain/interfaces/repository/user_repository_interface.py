from abc import ABC, abstractmethod

from app.shared.domain.entities import User

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def deactivate(self, user_id: str) -> User:
        pass

    @abstractmethod
    @staticmethod
    def to_entity(data: dict) -> User:
        pass