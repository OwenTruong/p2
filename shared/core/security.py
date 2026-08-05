import jwt
from fastapi import HTTPException, status
from shared.dtos.auth_user import AuthenticatedUser
from shared.core.config import get_shared_config

def verify_jwt_token(token: str) -> AuthenticatedUser:
    """
    Decodes and validates a JWT token 
    Raises 401 Unauthorized if the token is expired, modified, or malformed.
    """
    config = get_shared_config()
    try:
        payload = jwt.decode(token, config.jwt_secret_key, algorithms=[config.jwt_algorithm])
        
        user_id_raw = payload.get("sub")
        if not user_id_raw:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return AuthenticatedUser(
            user_id=int(user_id_raw),
            email=payload.get("email")
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or modified token",
            headers={"WWW-Authenticate": "Bearer"},
        )