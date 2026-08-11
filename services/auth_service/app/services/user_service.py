
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, user_repo : UserRepository | None = None):
        self.user_repo = user_repo or UserRepository()

    def get_user_by_id(self, user_id : str) -> User:
        return self.user_repo.find_by_id(user_id)