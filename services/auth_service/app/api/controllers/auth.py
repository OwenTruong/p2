from fastapi import APIRouter, Depends, Response, status, HTTPException
from app.dtos.auth import LoginRequest, AuthSuccessResponse
from app.dtos.user_dto import UserCreateRequestDTO
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.core.config import get_config

from shared.utils.exceptions import UniqueRowException

config = get_config()
router = APIRouter(prefix="/api/auth", tags=["Auth"])

def get_auth_service() -> AuthService:
    return AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    dto: UserCreateRequestDTO,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        saved_user = auth_service.save_user(dto)
        return {"status": "success", "detail": f"Account for user `{saved_user.email}` has been provisioned"}
    except UniqueRowException:
        raise HTTPException(status_code=409, detail="User with this email already exists")

@router.post("/login", response_model=AuthSuccessResponse, status_code=status.HTTP_200_OK)
def login(
    dto: LoginRequest, 
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    _, token = auth_service.authenticate_user(dto)
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,                            
        samesite="lax",                           
        max_age=config.jwt_expiration * 60,     
        path="/",
        secure=False
    )
    return AuthSuccessResponse()

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        path="/",
        secure=False
    )
    return {"status": "success", "detail": "Successfully logged out"}