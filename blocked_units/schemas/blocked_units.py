from typing import Optional

from pydantic import BaseModel
from blocked_units.schemas.passports import PassportSchemaResponse, PassportSchemaRequest, PassportSchemaPartialRequest
from company.schemas import CompanySchemaResponse
from datetime import datetime


class BlockedUnitSchemaResponse(BaseModel):
    id: int
    fio: str
    passports: Optional[PassportSchemaResponse] = None
    company: Optional[CompanySchemaResponse] = None
    reason: Optional[str] = None
    date_add_to_list: datetime

    class Config:
        from_attributes = True



class BlockedUnitSchemaRequest(BaseModel):
    fio: str
    passports: PassportSchemaRequest
    company_id: int
    reason: str


class BlockedUnitsSchemaPartialRequest(BaseModel):
    fio: Optional[str] = None
    passports: Optional[PassportSchemaPartialRequest] = None
    company_id: Optional[int] = None
    reason: Optional[str] = None
