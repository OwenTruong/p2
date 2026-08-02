from __future__ import annotations

from shared.data.Users import Users
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

  def save(self, email: str, password_hash: str, first_name: str, last_name: str) -> Users:
    query = f"INSERT INTO {self._table_name} (email, password_hash, first_name, last_name) VALUES(%s, %s, %s, %s) RETURNING *;"
    return self._execute_fetch_one(query, Users, values=[email, password_hash, first_name, last_name])

  def find_by_id(self, users_id: int) -> Users:
    query = f"SELECT * FROM {self._table_name} WHERE users_id=%s"
    return self._execute_fetch_one(query, Users, values=[users_id])

  def delete_by_id(self, users_id: int) -> None:
    query = f"DELETE FROM {self._table_name} WHERE users_id=%s"
    return self._execute(query, values=[users_id])