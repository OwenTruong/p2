
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserCreateRequestDTO(BaseModel):
  model_config = ConfigDict(extra="forbid")

  email: EmailStr = Field(examples=["john@example.com"])
  password: str = Field(min_length=8, max_length=128, examples=["password123"])
  first_name: str = Field(min_length=2, max_length=64, examples=["John"])
  last_name: str = Field(min_length=2, max_length=64, examples=["Doe"])

  @field_validator("email", mode="before")
  @classmethod
  def normalize_email(cls, value: str) -> str:
      return value.strip().lower()
  
  @field_validator("first_name", "last_name")
  @classmethod
  def validate_name(cls, value: str) -> str:
      value = value.strip()

      if not any(char.isalpha() for char in value):
          raise ValueError("Name must contain at least one letter")

      return value