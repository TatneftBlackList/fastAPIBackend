from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from users.models.users_permission import UserPermissionModel


class UserPermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_permission(self, permission: UserPermissionModel):
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
