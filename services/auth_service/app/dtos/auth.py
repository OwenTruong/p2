from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthSuccessResponse(BaseModel):
    status: str = "success"
    detail: str = "Authenticated session"