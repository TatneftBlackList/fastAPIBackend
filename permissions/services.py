from sqlalchemy.ext.asyncio import AsyncSession
from permissions.repositories import PermissionRepository
from permissions.permission_verification import PermissionVerification


class PermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission_repository = PermissionRepository(db)
        self.permission_verification = PermissionVerification(db)

    async def get_permissions(self, current_user: dict):
        if self.permission_verification.get_verification(current_user['permissions']):
            return await self.permission_repository.get_all_permissions()
