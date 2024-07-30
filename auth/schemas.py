from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    login: str
    password: str
    roleID: int


class User(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True
