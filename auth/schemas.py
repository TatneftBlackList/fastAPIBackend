from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    refresh_token: str
    role: str



class TokenData(BaseModel):
    login: Optional[str] = None
    permissions: Optional[List[str]] = None


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
