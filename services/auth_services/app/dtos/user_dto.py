
from pydantic import BaseModel, Field
from typing import Literal

class UserDTO(BaseModel):
  email: str = Field(examples=["john@example.com"])
  password: str = Field()
  first_name: str = Field(examples=["John"])
  last_name: str = Field(examples=["Doe"])