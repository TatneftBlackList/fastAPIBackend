from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from blocked_units.models.passports import PassportsModel


class PassportsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_passports(self, passport_id):
        passports = await self.db.execute(select(PassportsModel).where(PassportsModel.id == passport_id))
        return passports.scalar()

    async def create_passport(self, passport: PassportsModel):
        self.db.add(passport)
        await self.db.flush()
        await self.db.refresh(passport)
        return passport

    async def update_passport(self, passport: PassportsModel):
        self.db.add(passport)
        await self.db.flush()
        await self.db.refresh(passport)


    async def get_passport_by_number_and_seria(self, passport_number: str, passport_seria: str, exclude_passport_id: int):
        query = select(PassportsModel).where(
            PassportsModel.passport_number == passport_number,
            PassportsModel.passport_seria == passport_seria,
            PassportsModel.id != exclude_passport_id
        )
        result = await self.db.execute(query)
        return result.scalar()

    async def get_old_passport_by_seria_and_number(self, old_passport_number: str, old_passport_seria: str, exclude_passport_id: int):
        query = select(PassportsModel).where(
            PassportsModel.old_passport_number == old_passport_number,
            PassportsModel.old_passport_seria == old_passport_seria,
            PassportsModel.id != exclude_passport_id
        )
        result = await self.db.execute(query)
        return result.scalar()

    async def delete_passport(self, passport_id):
        passport = await self.db.execute(select(PassportsModel).where(PassportsModel.id == passport_id))

        result = passport.scalar()

        await self.db.delete(result)
        await self.db.commit()
