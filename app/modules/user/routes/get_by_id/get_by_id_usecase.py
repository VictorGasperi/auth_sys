from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository


class GetByIdUsecase():

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str):
        
        user = self.repo.get_by_id(user_id)

        return user
