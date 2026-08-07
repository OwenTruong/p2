from fastapi import APIRouter, Depends, status, HTTPException

from app.api.dependencies import get_current_user
from app.dtos.user_dto import UserResponseDTO
from app.models.user import User

from shared.utils.exceptions import UnexpectedException

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
)
def get_account_info(
    current_user: User = Depends(get_current_user),
) -> UserResponseDTO:
    if current_user.user_id == None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Invalid entity with email {current_user.email} received.")
    
    return UserResponseDTO(
        user_id=current_user.user_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        status=current_user.status,
    )