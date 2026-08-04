from typing import Literal

from shared.utils.exceptions import NoFetchedResultException

from ..models.user import User
from ..core.config import get_config

from shared.repositories.db_repository import DBRepository

class UserRepository(DBRepository):
  def __init__(self):
    table_name = 'users'

    config = get_config()
    super().__init__(table_name, config)

  def save(self, user: User) -> User:
    if user.user_id == None:
      query = f"INSERT INTO {self._table_name} (email, password_hash, first_name, last_name) VALUES(%s, %s, %s, %s) RETURNING *;"
      return self._execute_fetch_one(query, User, values=[user.email, user.password_hash, user.first_name, user.last_name])
    else:
      query = f"UPDATE {self._table_name} SET email=%s,password_hash=%s,first_name=%s,last_name=%s,status=%s WHERE user_id=%s RETURNING *;"
      return self._execute_fetch_one(query, User, values=[user.email, user.password_hash, user.first_name, user.last_name])

  def find_by_email(self, email: str) -> User | None:
      query = """
          SELECT *
          FROM users
          WHERE email = %s;
      """

      try:
          return self._execute_fetch_one(
              query,
              User,
              values=[email],
          )
      except NoFetchedResultException:
          return None
      
  def find_by_id(self, id: int) -> User | None:
    query = f"SELECT * FROM {self._table_name} WHERE user_id=%s"

    try:
      return self._execute_fetch_one(query, User, values=[id])
    except NoFetchedResultException:
      return None

  def update_status(
      self,
      user_id: int,
      status: Literal["Active", "Inactive"],
  ) -> User | None:
      query = """
          UPDATE users
          SET status = %s
          WHERE user_id = %s
          RETURNING
              user_id,
              email,
              password_hash,
              first_name,
              last_name,
              status;
      """

      try:
          return self._execute_fetch_one(
              query,
              User,
              values=[status, user_id],
          )
      except NoFetchedResultException:
          return None
      
  def delete_by_id(self, id: int) -> None:
    query = f"DELETE FROM {self._table_name} WHERE user_id=%s"
    return self._execute(query, values=[id])