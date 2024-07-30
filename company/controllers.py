from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from company.schemas import CompanySchemaResponse, CompanySchemaRequest
from typing import List
from db.session import get_session
from company.services import CompanyService

router = APIRouter()


@router.get("/company", summary="Возвращает массив компаний", status_code=status.HTTP_200_OK,
            response_model=List[CompanySchemaResponse])
async def get_company(session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)

    company = await service.get_all_company()

    return company


@router.post("/company", summary="Добавление компании", status_code=status.HTTP_201_CREATED,
             response_model=CompanySchemaResponse)
async def add_company(request: CompanySchemaRequest, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)

    new_company = await service.create_company(request)
    return new_company


@router.get("/company/{company_id}", summary="Возвращает компанию по ID", status_code=status.HTTP_200_OK,
            response_model=CompanySchemaResponse)
async def get_company(company_id: int, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)

    company = await service.get_company(company_id)
    return company


@router.patch("/company/{company_id}", summary="Обновление имени компании", status_code=status.HTTP_200_OK,
              response_model=CompanySchemaResponse)
async def update_company(request: CompanySchemaRequest, company_id: int, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)

    company = await service.update_company(company_id, request)
    return company


@router.delete("/company/{company_id}", summary="Удаление компании", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session)):
    service = CompanyService(session)

    await service.delete_company(company_id)

