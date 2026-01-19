from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository

class GetAllUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def __call__(self):
        return self.user_repository.get_all()