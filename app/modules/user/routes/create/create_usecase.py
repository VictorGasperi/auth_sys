from uuid import uuid4
from app.shared.domain.entities.user import CreateUser, User
from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository
from app.shared.utils.auth import get_password_hash
from app.shared.utils.time_utils import get_current_milis


class CreateUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: CreateUser):

        id = str(uuid4())
        is_active = True
        created_at_ms = get_current_milis()
        hashed_password = get_password_hash(user.password)

        user_to_create = User(
            id=id,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role,
            is_active=is_active,
            created_at_ms=created_at_ms
        )

        created_user = self.repo.create(user_to_create)

        return created_user