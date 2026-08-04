from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.dtos.auth import LoginRequest
from app.core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository | None = None):
        self.user_repo = user_repo or UserRepository()

    def authenticate_user(self, dto: LoginRequest) -> tuple[User, str]:
        user = self.user_repo.find_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid credentials"
            )

        if user.status != "Active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="account is inactive"
            )

        token = create_access_token(user.email)
        return user, token

