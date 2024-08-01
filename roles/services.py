from sqlalchemy.ext.asyncio import AsyncSession
from roles.repositories import RoleRepository
from permissions.permission_verification import PermissionVerification


class RolesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_repository = RoleRepository(db)
        self.permission_verification = PermissionVerification(db)

    async def get_all_roles(self, current_user: dict):
        if self.permission_verification.get_verification(current_user['permissions']):
            return await self.role_repository.get_all_roles()
