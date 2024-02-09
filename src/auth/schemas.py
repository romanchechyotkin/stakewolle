from pydantic import BaseModel, EmailStr, Field


class AuthUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class RegistrationResponse(BaseModel):
    email: EmailStr

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    user_id: str | None = None
    email: str | None = None