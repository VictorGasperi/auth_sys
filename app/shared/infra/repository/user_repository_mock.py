from datetime import datetime
from typing import List, Optional
from app.shared.domain.entities.user import User
from app.shared.domain.enums.role import ROLE
from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    users_list: List[User]

    def __init__(self):
        self.users_list = [
            User(
                id="93bc6ada-c0d1-7054-26ab-e17414c48ae3",
                email="admin@example.com",
                hashed_password="hashed_admin_pass",
                role=ROLE.ADMIN,
                is_active=True,
                created_at_ms=int(datetime.now().timestamp() * 1000)
            ),
            User(
                id="93bc6ada-c0d1-7054-26ab-e17454c48ae6",
                email="user1@example.com",
                hashed_password="hashed_user1_pass",
                role=ROLE.USER,
                is_active=True,
                created_at_ms=int(datetime.now().timestamp() * 1000)
            ),
            User(
                id="93bc6ada-c0e1-7054-26ab-e17414c48ae9",
                email="user2@example.com",
                hashed_password="hashed_user2_pass",
                role=ROLE.USER,
                is_active=False,
                created_at_ms=int(datetime.now().timestamp() * 1000)
            )
        ]

    
    def get_by_id(self, user_id: str) -> User:
        for user in self.users_list:
            if user.id == user_id:
                return user
            
        raise Exception(f"No user found for id {user_id}")

    
    def get_by_email(self, email: str) -> User:
        for user in self.users_list:
            if user.email == email:
                return user
        raise Exception(f"No user found for email {email}")
    
    def get_all(self) -> List[User]:
        return self.users_list

    
    def create(self, user: User) -> User:
        self.users_list.append(user)
        return user
    

    def update(self, user_id: str, new_email: Optional[str] = None, new_hashed_password: Optional[str] = None, new_role: Optional[ROLE] = None, new_is_active: Optional[bool] = None) -> User:
        user_to_update = self.get_by_id(user_id)

        if new_email is not None:
            user_to_update.email = new_email
        
        if new_hashed_password is not None:
            user_to_update.hashed_password = new_hashed_password

        if new_role is not None:
            user_to_update.role = new_role

        if new_is_active is not None:
            user_to_update.is_active = new_is_active

        return user_to_update