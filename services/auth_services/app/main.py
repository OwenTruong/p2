# System & Third Party
from pathlib import Path
import logging
import hashlib

from fastapi import FastAPI, Request, HTTPException, status, Response
from starlette.middleware.base import BaseHTTPMiddleware

# First Party
from .core.config import get_config
from .dtos.user_dto import UserDTO
from .models.user import User
from .repositories.user_repository import UserRepository

from shared.utils.exceptions import UniqueRowException


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'

config = get_config()

logging.basicConfig(level=logging.INFO if config.mode == "production" else logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

user_repository = UserRepository()

app = FastAPI(title="Auth Service")

@app.get("/health", status_code=status.HTTP_200_OK)
async def get_health():
    """Used to check if API is running"""
    try:
        return {
            "status": "healthy",
            }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# TODO: This is for testing purpose. JWT Auth and moving some of the logic code to service directory is needed.
@app.post("/api/auth/register", status_code=status.HTTP_200_OK)
async def register(payload: UserDTO):
    try:
        new_user = User(
            email = payload.email,
            password_hash = hashlib.pbkdf2_hmac(
                hash_name = 'sha256',
                password = payload.password.encode('utf-8'),
                salt = config.password_salt.encode('utf-8'),
                iterations = 600000
            ).hex(),
            first_name = payload.first_name,
            last_name = payload.last_name,
            status = 'Active'
        )
        user_repository.save(new_user)
        return {"status": "success", "detail": f"Account for user `{payload.email}` has been provisioned"}
    except UniqueRowException as exc:
        logging.info(exc)
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as exc:
        logging.error(exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")