from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.models import AuthModel


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_login(self, login: str):
        result = await self.db.execute(select(AuthModel).where(AuthModel.login == login))
        return result.scalar()

    async def create_user(self, user):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
