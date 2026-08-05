from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.dtos.auth_user import AuthenticatedUser
from shared.core.security import verify_jwt_token

security_bearer = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security_bearer)]) -> AuthenticatedUser:
    """
    Mandatory authentication dependency for protected endpoints.
    Rejects requests without a token or with invalid credentials with 401 Unauthorized.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Bearer authentication header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return verify_jwt_token(token=credentials.credentials)
