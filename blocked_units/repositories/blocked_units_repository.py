from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from blocked_units.models.blocked_units import BlockedUnitsModel
from blocked_units.models.passports import PassportsModel
from company.models import CompanyModel


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

    async def get_blocked_unit(self, blocked_unit_id: int):
        result = await self.db.execute(
            select(BlockedUnitsModel)
            .where(BlockedUnitsModel.id == blocked_unit_id)
            .options(joinedload(BlockedUnitsModel.passports_rel))
        )
        return result.scalar()


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

    async def delete_blocked_units(self, blocked_unit: BlockedUnitsModel):
        await self.db.delete(blocked_unit)
        await self.db.commit()

    async def search_blocked_units(
        self,
        fio: Optional[str] = None,
        passport_number: Optional[str] = None,
        passport_seria: Optional[str] = None,
        company_name: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> List[BlockedUnitsModel]:
        query = (select(BlockedUnitsModel)
                 .options(joinedload(BlockedUnitsModel.passports_rel),
                          joinedload(BlockedUnitsModel.company_rel)))


        if fio:
            query = query.where(BlockedUnitsModel.fio.ilike(f'%{fio}%'))
        if passport_number:
            query = query.where(BlockedUnitsModel
                                .passports_rel.has(PassportsModel.passport_number == passport_number))
        if passport_seria:
            query = query.where(BlockedUnitsModel
                                .passports_rel.has(PassportsModel.passport_seria == passport_seria))
        if company_name:
            query = query.where(BlockedUnitsModel
                                .company_rel.has(CompanyModel.name.ilike(f'%{company_name}%')))
        if reason:
            query = query.where(BlockedUnitsModel.reason.ilike(f'%{reason}%'))

        result = await self.db.execute(query)
        return result.scalars().all()
