from sqlalchemy.ext.asyncio import AsyncSession
from permissions.models import PermissionModel
from sqlalchemy.future import select


class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_permissions(self):
        permissions = await self.db.execute(select(PermissionModel))
        return permissions.scalars().all()
