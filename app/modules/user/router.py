from fastapi import APIRouter, Request

from app.modules.user.routes.get_all.get_all_presenter import get_all_handler


router = APIRouter()

@router.get("/get_all")
def get_all(req: Request):
    return get_all_handler(req)
