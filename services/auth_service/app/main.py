# System & Third Party
from pathlib import Path
import logging
import hashlib

from fastapi import FastAPI, Request, HTTPException, status, Response
from starlette.middleware.base import BaseHTTPMiddleware

# First Party
from .core.config import get_config
from .dtos.user_dto import UserCreateRequestDTO
from .models.user import User
from .repositories.user_repository import UserRepository
from .api.controllers import auth

from shared.utils.exceptions import UniqueRowException


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static'

config = get_config()

logging.basicConfig(level=logging.INFO if config.mode == "production" else logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

user_repository = UserRepository()

app = FastAPI(title="Auth Service")

app.include_router(auth.router)

@app.get("/health", status_code=status.HTTP_200_OK)
async def get_health():
    """Used to check if API is running"""
    try:
        return {
            "status": "healthy",
            }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))