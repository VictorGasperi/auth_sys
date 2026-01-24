from fastapi import HTTPException, Request
from app.modules.user.routes.get_by_id.get_by_id_usecase import GetByIdUsecase
from app.modules.user.routes.get_by_id.get_by_id_viewmodel import GetByIdViewmodel


class GetByIdController():

    def __init__(self, usecase: GetByIdUsecase):
        self.usecase = usecase

    def __call__(self, req: Request):
        
        try:

            user_id = req.query_params.get('user_id', None)

            if not user_id:
                raise HTTPException(status_code=400, detail="user_id must be provided on request params.")

            user = self.usecase(user_id)
            viewmodel = GetByIdViewmodel(user)
            return viewmodel.to_dict()
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error while returning user_id -> INFO: " + str(e))
