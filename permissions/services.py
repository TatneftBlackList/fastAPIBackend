from sqlalchemy.ext.asyncio import AsyncSession
from permissions.repositories import PermissionRepository


class PermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission_repository = PermissionRepository(db)

    async def get_permissions(self):
        return await self.permission_repository.get_all_permissions()
