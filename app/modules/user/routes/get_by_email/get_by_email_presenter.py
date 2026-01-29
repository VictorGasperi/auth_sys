from fastapi import Request
from app.modules.user.routes.get_by_email.get_by_email_controller import GetByEmailController
from app.modules.user.routes.get_by_email.get_by_email_usecase import GetByEmailUsecase
from app.shared.environments import Environments


repo = Environments.get_user_repo()()
usecase = GetByEmailUsecase(repo)
controller = GetByEmailController(usecase)

def get_by_email_handler(req: Request):

    response = controller(req)

    return response