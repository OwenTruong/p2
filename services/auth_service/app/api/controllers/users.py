from fastapi import APIRouter, Depends, status

from app.services.user_service import UserService
from shared.dependencies.auth import get_current_user
from app.dtos.user_dto import UserResponseDTO

from shared.dtos.errors import ApiErrorDTO
from shared.dtos.auth_user import AuthenticatedUser
from shared.exceptions.exceptions import ApiException

router = APIRouter(prefix="/api/users", tags=["Users"])

def get_user_service() -> UserService:
    return UserService()

@router.get(
    "/me",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
)
def get_account_info(
    current_user: AuthenticatedUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)

) -> UserResponseDTO:

    if current_user.user_id is None:
        raise ApiException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            errors=[
                ApiErrorDTO(message=f"Invalid entity with email {current_user.email} received.")
            ]
        )

    user_details = user_service.get_user_by_id(current_user.user_id)

    return UserResponseDTO(
        user_id=user_details.user_id,
        email=user_details.email,
        first_name=user_details.first_name,
        last_name=user_details.last_name,
        status=user_details.status,
    )