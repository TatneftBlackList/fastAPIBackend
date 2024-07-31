from typing import Optional

from pydantic import BaseModel


class UsersSchemaResponse(BaseModel):
    id: int
    job_number: str
    first_name: str
    last_name: str


class UsersSchemaRequest(BaseModel):
    job_number: str
    first_name: str
    last_name: str


class UsersSchemaRequestPartial(BaseModel):
    job_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
