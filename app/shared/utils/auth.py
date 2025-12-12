from app.shared.environments import Environments


SECRET_KEY = Environments.get_envs().secret_key
ALGORITHM = Environments.get_envs().algorithm
ACCESS_TOKEN_EXPIRATION_MIN = 30

def verify_password(plain_password: str, hashed_password: str):
    