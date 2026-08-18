import jwt
from fastapi import status
from shared.dtos.auth_user import AuthenticatedUser
from shared.core.config import get_shared_config
from shared.dtos.errors import ApiErrorDTO
from shared.exceptions.exceptions import UnauthorizedException

def verify_jwt_token(token: str) -> AuthenticatedUser:
    """
    Decodes and validates a JWT token 
    Raises 401 Unauthorized if the token is expired, modified, or malformed.
    """
    config = get_shared_config()
    try:
        return jwt.decode(token, config.jwt_secret_key, algorithms=[config.jwt_algorithm])
        
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    
    except (jwt.PyJWTError, ValueError):
        raise UnauthorizedException("Invalid or modified token")