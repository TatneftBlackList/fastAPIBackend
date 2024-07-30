from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from permissions.models import PermissionModel
from permissions.enums import PermissionEnums


async def seed_permissions(db: AsyncSession) -> None:
    async with db.begin():
        permissions = [PermissionEnums.CREATE, PermissionEnums.READ, PermissionEnums.UPDATE, PermissionEnums.DELETE]

        for permission in permissions:

            result = await db.execute(select(PermissionModel).filter_by(name=permission))

            existing_permission = result.scalar_one_or_none()

            if existing_permission is None:

                new_permission = PermissionModel(name=permission)
                db.add(new_permission)

        await db.commit()
