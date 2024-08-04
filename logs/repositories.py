from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from logs.models import UserRequestLogModel
from sqlalchemy.future import select
from auth.models import AuthModel



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

    async def get_logs(self):
        result = await self.db.execute(
            select(UserRequestLogModel)
            .options(joinedload(UserRequestLogModel.user))
            .options(joinedload(UserRequestLogModel.user).joinedload(AuthModel.user_rel))
        )
        return result.scalars().all()

    async def get_log(self, log_id: int):
        result = await self.db.execute(
            select(UserRequestLogModel).where(UserRequestLogModel.id == log_id)
            .options(joinedload(UserRequestLogModel.user))
            .options(joinedload(UserRequestLogModel.user).joinedload(AuthModel.user_rel))
        )
        return result.scalar()


    async def get_logs_for_user(self, user_id: int):
        result = await self.db.execute(
            select(UserRequestLogModel)
            .options(
                joinedload(UserRequestLogModel.user)
                .joinedload(AuthModel.user_rel)
            )
            .where(AuthModel.user_id == user_id)
        )
        return result.scalars().all()
