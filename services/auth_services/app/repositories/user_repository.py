from __future__ import annotations

from services.auth_services.app.data.User import User
from shared.repositories.db_repository import DBRepository

class UserRepository(DBRepository):
  def __init__(self):
    table_name = "users"
    # see https://www.postgresql.org/docs/current/sql-do.html
    table_query = f"""
      DO $$
      BEGIN
        IF NOT EXISTS (Select 1 FROM pg_type WHERE typname = 'user_status') THEN
          CREATE TYPE user_status as ENUM ('Active', 'Inactive');
        END IF;
      END $$;

      CREATE TABLE IF NOT EXISTS {table_name} (
        users_id BIGSERIAL PRIMARY KEY,
        email VARCHAR(128) NOT NULL UNIQUE,
        password_hash VARCHAR(128) NOT NULL,
        first_name VARCHAR(64) NOT NULL,
        last_name VARCHAR(64) NOT NULL,
        status user_status NOT NULL DEFAULT 'Active'
      );
    """

    super().__init__(table_name, table_query)

  def save(self, user: User) -> User:
    if user.user_id == None:
      query = f"INSERT INTO {self._table_name} (email, password_hash, first_name, last_name) VALUES(%s, %s, %s, %s) RETURNING *;"
      return self._execute_fetch_one(query, User, values=[user.email, user.password_hash, user.first_name, user.last_name])
    else:
      query = f"UPDATE {self._table_name} SET email=%s,password_hash=%s,first_name=%s,last_name=%s,status=%s WHERE user_id=%s RETURNING *;"
      return self._execute_fetch_one(query, User, values=[user.email, user.password_hash, user.first_name, user.last_name, user.status, user.user_id])

  def find_by_id(self, id: int) -> User:
    query = f"SELECT * FROM {self._table_name} WHERE users_id=%s"
    return self._execute_fetch_one(query, User, values=[id])

  def delete_by_id(self, id: int) -> None:
    query = f"DELETE FROM {self._table_name} WHERE users_id=%s"
    return self._execute(query, values=[id])