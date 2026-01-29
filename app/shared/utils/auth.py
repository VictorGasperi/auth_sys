from app.shared.environments import Environments
from passlib.context import CryptContext

SECRET_KEY = Environments.get_envs().secret_key
ALGORITHM = Environments.get_envs().algorithm
ACCESS_TOKEN_EXPIRATION_MIN = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(plain_password: str):
    return pwd_context.hash(plain_password)