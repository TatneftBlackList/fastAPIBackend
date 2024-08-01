from sqlalchemy.ext.asyncio import AsyncSession
from logs.models import UserRequestLogModel



class UserRequestLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_log(self, user_id: int, path: str, method: str, response_status: int):
        log = UserRequestLogModel(
            user_id=user_id,
            path=path,
            method=method,
            response_status=response_status
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log
