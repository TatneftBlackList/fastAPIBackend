from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.models import AuthModel
from permissions.models import PermissionModel
from users.models.users_permission import UserPermissionModel


class UserPermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_permission(self, permission: UserPermissionModel):
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)

    async def get_permissions_from_user(self, auth: AuthModel):
        result = await self.db.execute(
            select(PermissionModel.name)
            .join(UserPermissionModel)
            .where(UserPermissionModel.user_id == auth.user_id)
        )
        return result.scalars().all()
