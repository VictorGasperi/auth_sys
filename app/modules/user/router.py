router = APIRouter()

@router.get("/get_all")
def get_all():
    return {"status": "ok"}
