from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from roles.models import RolesModel


class RoleRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_roles(self):
        roles = await self.db.execute(select(RolesModel))
        return roles.scalars().all()

