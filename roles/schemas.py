from pydantic import BaseModel


class RolesSchemas(BaseModel):
    id: int
    name: str
