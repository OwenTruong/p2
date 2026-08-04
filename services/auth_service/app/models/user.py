
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class User(BaseModel):
  user_id: int | None  = Field(default=None, ge=1) # 0 represents that the user is new and does not exist in db yet. BIGSERIAL start generating id at 1.
  email: EmailStr = Field(examples=["john@example.com"])
  password_hash: str = Field(min_length=1, max_length=128)
  first_name: str = Field(examples=["John"], min_length=1, max_length=64)
  last_name: str = Field(examples=["Doe"], min_length=1, max_length=64)
  status: Literal["Active", "Inactive"] = Field(default="Active", examples=["Active"])