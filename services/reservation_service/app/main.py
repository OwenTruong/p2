# System & Third Party
from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .api.controllers import reservations
from shared.exceptions.exception_handlers import register_exception_handlers

# First Party
from .core.config import get_config

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

config = get_config()

logging.basicConfig(
    level=logging.INFO if config.mode == "production" else logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Reservation Service")

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        config.cors_origin_url
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reservations.router)

@app.get("/health", status_code=status.HTTP_200_OK)
async def get_health():
    """Used to check if API is running."""
    try:
        return {
            "status": "healthy",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))