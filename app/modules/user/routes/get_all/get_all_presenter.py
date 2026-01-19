from app.modules.user.routes.get_all.get_all_controller import GetAllController
from app.shared.environments import Environments
from app.modules.user.routes.get_all.get_all_usecase import GetAllUseCase
from fastapi import Request

repo = Environments.get_user_repo()()
usecase = GetAllUseCase(user_repository=repo)
controller = GetAllController(usecase=usecase)

def handler(request: Request):

    response = controller(request)
    return response