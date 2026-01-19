from typing import List
from app.shared.domain.entities.user import User
class GetAllViewModel:
    def __init__(self, users: List[User]):
        self.users = users

    def to_dict(self):
        return {
            "users": [user.to_dict() for user in self.users],
            "message": 'The users were retrieved'
        }   