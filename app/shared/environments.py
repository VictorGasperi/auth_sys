from enum import Enum
import os

from app.shared.domain.interfaces.repository.user_repository_interface import IUserRepository

class STAGE(Enum):
    TEST = "test"
    DEV = "dev"

class Environments:
    stage: STAGE
    pgsql_url: str
    mss_name: str
    secret_key: str
    algorithm: str

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.TEST.value

    def load_envs(self):
        if "STAGE" not in os.environ:
            self._configure_local()

        self.stage = STAGE(os.environ.get("STAGE"))
        self.pgsql_url = os.environ.get("PGSQL_URL")
        self.mss_name = os.environ.get("MSS_NAME")
        self.secret_key = os.environ.get("SECRET_KEY")
        self.algorithm = os.environ.get("ALGORITHM")

    @staticmethod
    def get_envs() -> "Environments":
        envs = Environments()
        envs.load_envs()
        return envs
        
    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from app.shared.infra.repository.adapters.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        elif Environments.get_envs().stage == STAGE.DEV:
            from app.shared.infra.repository.adapters.user_repository_pgsql import UserRepositoryPgsql
            return UserRepositoryPgsql
        else:
            raise Exception(f"No repository found for the stage '{Environments.get_envs().stage}'")