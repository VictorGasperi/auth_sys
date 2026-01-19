from app.modules.user.routes.get_all.get_all_usecase import GetAllUseCase
from app.modules.user.routes.get_all.get_all_viewmodel import GetAllViewModel
from fastapi import Request, HTTPException
class GetAllController:
    def __init__(self, usecase: GetAllUseCase):
        self.usecase = usecase

    def __call__(self, request: Request):
        try:
            users = self.usecase()
            viewmodel = GetAllViewModel(users=users)
            return viewmodel.to_dict()

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error while returning all users -> INFO: " + str(e))