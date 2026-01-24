from fastapi import Request
from app.modules.user.routes.get_by_id.get_by_id_controller import GetByIdController
from app.modules.user.routes.get_by_id.get_by_id_usecase import GetByIdUsecase
from app.shared.environments import Environments


repo = Environments.get_user_repo()()
usecase = GetByIdUsecase(repo)
controller = GetByIdController(usecase)

def get_by_id_handler(req: Request):

    response = controller(req)
    return response