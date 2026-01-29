from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository


class GetByEmailUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str):

        user = self.repo.get_by_email(email)

        return user