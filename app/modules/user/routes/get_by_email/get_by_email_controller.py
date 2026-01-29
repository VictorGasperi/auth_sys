from fastapi import HTTPException, Request
from app.modules.user.routes.get_by_email.get_by_email_usecase import GetByEmailUsecase
from app.modules.user.routes.get_by_email.get_by_email_viewmodel import GetByEmailViewmodel


class GetByEmailController:

    def __init__(self, usecase: GetByEmailUsecase):
        self.usecase = usecase

    def __call__(self, req: Request):

        try:

            user_email = req.query_params.get('email', None)

            if not user_email:
                raise HTTPException(status_code=400, detail="email must be provided on request params.")
            
            user = self.usecase(user_email)
            viewmodel = GetByEmailViewmodel(user)
            return viewmodel.to_dict()
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error while returning user_id -> INFO: " + str(e))