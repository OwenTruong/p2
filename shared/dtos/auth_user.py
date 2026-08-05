from pydantic import BaseModel, Field

class AuthenticatedUser(BaseModel):
    user_id: int = Field(description="User ID extracted directly from token subject")
    email: str | None = Field(default=None)