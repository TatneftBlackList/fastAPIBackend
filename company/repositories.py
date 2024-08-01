from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from company.models import CompanyModel


class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_company(self):
        company = await self.db.execute(select(CompanyModel))
        return company.scalars().all()

    async def create_company(self, company: CompanyModel):
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def get_company(self, company_id):
        company = await self.db.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        return company.scalar()

    async def update_company(self, company: CompanyModel):
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def delete_company(self, company: CompanyModel):
        await self.db.delete(company)
        await self.db.commit()
