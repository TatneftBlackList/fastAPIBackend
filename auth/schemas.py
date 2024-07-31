from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    job_number: str
    login: str
    password: str
    roleID: int
    permissions_id: List[int]


class User(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True
