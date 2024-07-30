# db/seed.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from roles.models import RolesModel
from roles.enums import RolesEnum


async def seed_roles(db: AsyncSession):
    async with db.begin():
        roles = [RolesEnum.ADMIN, RolesEnum.USER]

        for role in roles:
            result = await db.execute(select(RolesModel).filter_by(name=role))
            existing_role = result.scalar_one_or_none()

            if existing_role is None:
                new_role = RolesModel(name=role)
                db.add(new_role)

        await db.commit()
