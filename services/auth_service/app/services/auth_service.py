from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.dtos.auth import LoginRequest
from app.core.security import verify_password, create_access_token, hash_password
from app.dtos.user_dto import UserCreateRequestDTO, UserResponseDTO
from shared.dtos.errors import ApiErrorDTO
from shared.exceptions.exceptions import ApiException, EmailAlreadyExistsException
from shared.utils.exceptions import UniqueRowException


class AuthService:
    def __init__(self, user_repo: UserRepository | None = None):
        self.user_repo = user_repo or UserRepository()

    def authenticate_user(self, dto: LoginRequest) -> tuple[User, str]:
        user = self.user_repo.find_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password_hash):
            raise ApiException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                errors=[
                    ApiErrorDTO(message="Invalid email or password.")
                ]
            )

        if user.status != "Active":
            raise ApiException(
                status_code=status.HTTP_403_FORBIDDEN,
                errors=[
                    ApiErrorDTO(message="Account is inactive.")
                ]
            )

        assert user.user_id is not None, "Database record must have an ID"
        token = create_access_token(user.user_id, user.email)
        return user, token

    def save_user(self, dto: UserCreateRequestDTO) -> User:
        user = User(
                    email=dto.email,
                    password_hash=hash_password(dto.password),
                    first_name=dto.first_name,
                    last_name=dto.last_name
                )
        try:      
            saved_user = self.user_repo.save(user)
            return UserResponseDTO(
                user_id=saved_user.user_id,
                email=saved_user.email,
                first_name=saved_user.first_name,
                last_name=saved_user.last_name,
                status=saved_user.status
            )
        
        except UniqueRowException:
            raise EmailAlreadyExistsException() from None