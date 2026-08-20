from pydantic import Field
from typing import Literal
from shared.dtos.db_config import DBConfig

class Config(DBConfig):
  mode: Literal["Production", "Development"] = Field(examples=["Production", "Development"])
  cors_origin_url: str = Field(examples=["http://localhost:8080"])
  listing_service_url: str