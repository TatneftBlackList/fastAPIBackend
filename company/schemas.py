from pydantic import BaseModel


class CompanySchemaResponse(BaseModel):
    id: int
    name: str


class CompanySchemaRequest(BaseModel):
    name: str
