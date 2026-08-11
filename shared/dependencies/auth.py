from fastapi import Request, status
from shared.core.security import verify_jwt_token
from shared.dtos.auth_user import AuthenticatedUser
from shared.dtos.errors import ApiErrorDTO
from shared.exceptions.exceptions import ApiException

def get_current_user(request: Request) -> AuthenticatedUser:
    token = request.cookies.get("access_token")
    if not token:
        raise ApiException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            errors=[
                ApiErrorDTO(message="Missing or invalid JWT.")
            ]
        )

    payload = verify_jwt_token(token)
    if not payload or "sub" not in payload:
        raise ApiException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            errors=[
                ApiErrorDTO(message="Missing or invalid JWT.")
            ]
        )

    return AuthenticatedUser(
        user_id=int(payload["sub"]),
        email=payload["email"]
    )