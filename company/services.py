from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from company.repositories import CompanyRepository
from company.models import CompanyModel
from fastapi import HTTPException


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.company_repository = CompanyRepository(db)


    async def get_all_company(self):
        return await self.company_repository.get_all_company()

    async def create_company(self, company):
        new_company = CompanyModel(
            name=company.name
        )
        return await self.company_repository.create_company(new_company)

    async def get_company(self, company_id):
        company = await self.company_repository.get_company(company_id)

        if not company:
            raise HTTPException(
                detail='Company not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
        return company

    async def update_company(self, company_id, company):
        existing_company = await self.company_repository.get_company(company_id)

        if not existing_company:
            raise HTTPException(
                detail='Company not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        existing_company.name = company.name
        return await self.company_repository.update_company(existing_company)

    async def delete_company(self, company_id):
        company = await self.company_repository.get_company(company_id)

        if not company:
            raise HTTPException(
                detail='Company not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
        await self.company_repository.delete_company(company)
