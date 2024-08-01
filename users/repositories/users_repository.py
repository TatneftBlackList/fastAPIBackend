from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.models.users import UserModel


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserModel):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_users(self):
        users = await self.db.execute(select(UserModel))
        return users.scalars().all()

    async def get_user_by_job_number(self, job_number):
        user = await self.db.execute(select(UserModel).where(UserModel.job_number == job_number))
        return user.scalar()

    async def get_user_by_id(self, user_id):
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return user.scalar()

    async def update_user(self, user: UserModel):
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: UserModel):
        await self.db.delete(user)
        await self.db.commit()
