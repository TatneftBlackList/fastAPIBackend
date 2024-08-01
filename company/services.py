from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from company.schemas import CompanySchemaRequest
from company.repositories import CompanyRepository
from company.models import CompanyModel
from fastapi import HTTPException

from permissions.permission_verification import PermissionVerification


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.company_repository = CompanyRepository(db)
        self.permission_verification = PermissionVerification(db)


    async def get_all_company(self, current_user: dict):
        if self.permission_verification.get_verification(current_user['permissions']):
            return await self.company_repository.get_all_company()

    async def create_company(self, request: CompanySchemaRequest, current_user: dict):
        if self.permission_verification.post_verification(current_user['permissions']):
            new_company = CompanyModel(
                name=request.name
            )
            return await self.company_repository.create_company(new_company)

    async def get_company(self, company_id: int, current_user: dict):
        if self.permission_verification.get_verification(current_user['permissions']):
            company = await self.company_repository.get_company(company_id)

            if not company:
                raise HTTPException(
                    detail='Company not found',
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return company

    async def update_company(self, company_id: int, request: CompanySchemaRequest, current_user: dict):
        if self.permission_verification.put_patch_verification(current_user['permissions']):
            existing_company = await self.company_repository.get_company(company_id)

            if not existing_company:
                raise HTTPException(
                    detail='Company not found',
                    status_code=status.HTTP_404_NOT_FOUND
                )

            existing_company.name = request.name
            return await self.company_repository.update_company(existing_company)

    async def delete_company(self, company_id: int, current_user: dict):
        if self.permission_verification.delete_verification(current_user['permissions']):
            company = await self.company_repository.get_company(company_id)

            if not company:
                raise HTTPException(
                    detail='Company not found',
                    status_code=status.HTTP_404_NOT_FOUND
                )
            await self.company_repository.delete_company(company)
