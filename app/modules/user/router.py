from fastapi import APIRouter, Query, Request

from app.modules.user.routes.create.create_presenter import create_handler
from app.modules.user.routes.get_all.get_all_presenter import get_all_handler
from app.modules.user.routes.get_by_email.get_by_email_presenter import get_by_email_handler
from app.modules.user.routes.get_by_id.get_by_id_presenter import get_by_id_handler
from app.shared.domain.entities.user import CreateUser


router = APIRouter()

@router.get("/get_all")
def get_all(req: Request):
    return get_all_handler(req)

@router.get("/get_by_id")
def get_by_id(req: Request, user_id: str = Query(..., description="ID do usuário")):
    return get_by_id_handler(req)

@router.get("/get_by_email")
def get_by_email(req: Request, email: str = Query(..., description="E-mail do usuário")):
    return get_by_email_handler(req)

@router.post("/create")
async def create(req: Request, user_to_create: CreateUser):
    return await create_handler(req)