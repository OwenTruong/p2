import os
from dotenv import load_dotenv
from ..dtos.shared_config import SharedConfig

load_dotenv()

__shared_config = SharedConfig(
    jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS"),
    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "secretkey")
)

def get_shared_config() -> SharedConfig:
    return __shared_config