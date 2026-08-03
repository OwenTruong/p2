
from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
  user_id: int | None  = Field(default=None) # 0 represents that the user is new and does not exist in db yet. BIGSERIAL start generating id at 1.
  email: str = Field(examples=["john@example.com"])
  password_hash: str = Field()
  first_name: str = Field(examples=["John"])
  last_name: str = Field(examples=["Doe"])
  status: Literal["Active", "Inactive"] = Field(examples=["Active"])