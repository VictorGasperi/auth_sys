from app.modules.user.router import router
from app.shared.environments import Environments
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title=Environments.get_envs().mss_name + "-USER",
        version="1.0.0",
        root_path='/user'
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(router)
    return app

app = create_app()