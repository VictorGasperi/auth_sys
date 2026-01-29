from app.shared.domain.entities.user import User

class GetByEmailViewmodel:

    def __init__(self, user: User):
        self.user = user

    def to_dict(self) -> dict:

        return {
            "user": self.user.to_dict(),
            "message": "The user was retrieved"
        }