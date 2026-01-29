from fastapi import HTTPException, Request
from app.modules.user.routes.create.create_usecase import CreateUsecase
from app.modules.user.routes.create.create_viewmodel import CreateViewmodel
from app.shared.domain.entities.user import CreateUser
from app.shared.domain.enums.role import ROLE


class CreateController:

    def __init__(self, usecase: CreateUsecase):
        self.usecase = usecase

    async def __call__(self, req: Request):

        try:

            body: dict = await req.json()
            email = body.get('email', None)
            password = body.get('password', None)
            role = ROLE(str(body.get('role')).upper()) if str(body.get('role')).upper() in ROLE.__members__ else None

            if not email or not password or role is None:
                raise HTTPException(status_code=400, detail='email, password and role of user must be provided in the request.')

            user_to_create = CreateUser(
                email=email,
                password=password,
                role=role
            )

            created_user = self.usecase(user_to_create)
            viewmodel = CreateViewmodel(created_user)

            return viewmodel.to_dict()
        
        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error while creating user -> INFO: " + str(e))