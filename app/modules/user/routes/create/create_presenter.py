from fastapi import Request
from app.modules.user.routes.create.create_controller import CreateController
from app.modules.user.routes.create.create_usecase import CreateUsecase
from app.shared.environments import Environments


repo = Environments.get_user_repo()()
usecase = CreateUsecase(repo)
controller = CreateController(usecase)

async def create_handler(req: Request):

    response = await controller(req)

    return response