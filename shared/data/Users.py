
from pydantic import BaseModel, Field
from typing import Literal

class Users(BaseModel):
  users_id: int = Field()
  email: str = Field(examples=["john@example.com"])
  password_hash: str = Field()
  first_name: str = Field(examples=["John"])
  last_name: str = Field(examples=["Doe"])
  status: Literal["Active", "Inactive"] = Field(examples=["Active"])