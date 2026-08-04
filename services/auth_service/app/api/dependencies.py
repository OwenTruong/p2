from fastapi import Request, HTTPException, status
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User

user_repo = UserRepository()

def get_current_user(request: Request) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing or invalid JWT"
        )

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing or invalid JWT"
        )

    user = user_repo.find_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user no longer exists"
        )

    return user