from pydantic import Field
from typing import Literal
from shared.dtos.db_config import DBConfig

class Config(DBConfig):
  mode: Literal["Production", "Development"] = Field(examples=["Production", "Development"])
  password_salt: str = Field()
  jwt_algorithm: str = Field()
  jwt_secret_key: str = Field()
  jwt_expiration: int 