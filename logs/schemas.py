from pydantic import BaseModel
from datetime import datetime
from users.schemas import UsersSchemaResponse


class LogsSchema(BaseModel):
    id: int
    user: UsersSchemaResponse
    path: str
    method: str
    timestamp: datetime
    response_status: int
