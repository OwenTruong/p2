import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import get_config

config = get_config()

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        config.password_salt.encode("utf-8"),
        100000
    ).hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(user_id: int, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.jwt_expiration)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }
    return jwt.encode(payload, config.jwt_secret_key, algorithm=config.jwt_algorithm)