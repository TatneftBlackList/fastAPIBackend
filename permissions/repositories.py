from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import AuthModel
from permissions.enums import PermissionEnums
from permissions.models import PermissionModel
from sqlalchemy.future import select

from users.models.users import UserModel
from users.models.users_permission import UserPermissionModel


class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_permissions(self):
        permissions = await self.db.execute(select(PermissionModel))
        return permissions.scalars().all()

    async def has_permission(self, user_id: int, permission: PermissionEnums):
        result = await self.db.execute(
            select(exists().where(
                UserPermissionModel.user_id == user_id,
                UserPermissionModel.permission_rel.has(PermissionModel.name == permission)
            ))
        )
        return result.scalar()
