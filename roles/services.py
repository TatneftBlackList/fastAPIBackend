from sqlalchemy.ext.asyncio import AsyncSession
from roles.repositories import RoleRepository


class RolesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_repository = RoleRepository(db)

    async def get_all_roles(self):
        return await self.role_repository.get_all_roles()
