from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from blocked_units.models.blocked_units import BlockedUnitsModel


class BlockedUnitsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_blocked_units(self):
        result = await self.db.execute(
            select(BlockedUnitsModel)
            .options(joinedload(BlockedUnitsModel.passports_rel))
            .options(joinedload(BlockedUnitsModel.company_rel))
        )
        return result.scalars().all()


    async def create_blocked_unit(self, blocked_unit: BlockedUnitsModel):
        self.db.add(blocked_unit)
        await self.db.flush()
        await self.db.refresh(blocked_unit)
        return blocked_unit


    async def get_blocked_unit_by_id(self, blocked_unit_id):
        result = await self.db.execute(
            select(BlockedUnitsModel).where(BlockedUnitsModel.id == blocked_unit_id)
            .options(joinedload(BlockedUnitsModel.passports_rel))
            .options(joinedload(BlockedUnitsModel.company_rel))
        )
        return result.scalar()

    async def update_blocked_unit(self, blocked_unit: BlockedUnitsModel):
        self.db.add(blocked_unit)
        await self.db.flush()
        await self.db.refresh(blocked_unit)
