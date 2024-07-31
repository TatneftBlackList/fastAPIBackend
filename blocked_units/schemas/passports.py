from typing import Optional

from pydantic import BaseModel


class PassportSchemaResponse(BaseModel):
    id: int
    passport_seria: Optional[str] = None
    passport_number: Optional[str] = None
    old_passport_number: Optional[str] = None
    old_passport_seria: Optional[str] = None


class PassportSchemaRequest(BaseModel):
    passport_seria: str
    passport_number: str
    old_passport_number: Optional[str] = None
    old_passport_seria: Optional[str] = None


class PassportSchemaPartialRequest(BaseModel):
    passport_seria: Optional[str] = None
    passport_number: Optional[str] = None
    old_passport_number: Optional[str] = None
    old_passport_seria: Optional[str] = None
