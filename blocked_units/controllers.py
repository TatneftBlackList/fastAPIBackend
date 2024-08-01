from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from db.session import get_session
from blocked_units.schemas.blocked_units import (BlockedUnitSchemaResponse, BlockedUnitSchemaRequest,
                                                 BlockedUnitsSchemaPartialRequest)
from blocked_units.services.blocked_units_service import BlockedUnitsService

router = APIRouter()


@router.get("/blockedUnits", summary="Возвращает массив заблокированных пользователей",
            status_code=status.HTTP_200_OK, response_model=List[BlockedUnitSchemaResponse])
async def get_blocked_units(session: AsyncSession = Depends(get_session)):
    service = BlockedUnitsService(session)
    blocked_units = await service.get_blocked_units()

    return blocked_units


@router.post("/blockedUnits", summary="Добавление пользователя",
             status_code=status.HTTP_201_CREATED, response_model=BlockedUnitSchemaResponse)
async def add_blocked_units(request: BlockedUnitSchemaRequest, session: AsyncSession = Depends(get_session)):
    service = BlockedUnitsService(session)

    new_blocked_units = await service.add_blocked_units(request)

    return new_blocked_units


@router.get("/blockedUnits/{blocked_unit_id}", summary="Возвращает заблокированного пользователя по ID",
            status_code=status.HTTP_200_OK, response_model=BlockedUnitSchemaResponse)
async def get_blocked_unit(blocked_unit_id: int, session: AsyncSession = Depends(get_session)):
    service = BlockedUnitsService(session)

    blocked_unit = await service.get_unit_by_id(blocked_unit_id)

    return blocked_unit


@router.put("/blockedUnits/{blocked_unit_id}", summary="Полное обновление ресурса по ID",
            status_code=status.HTTP_200_OK, response_model=BlockedUnitSchemaResponse)
async def update_blocked_units(request: BlockedUnitSchemaRequest, blocked_unit_id: int,
                               session: AsyncSession = Depends(get_session)):
    service = BlockedUnitsService(session)

    update_unit = await service.update_blocked_units(request, blocked_unit_id)

    return update_unit


@router.patch("/blockedUnits/{blocked_unit_id}", summary="Частичное обновление ресурса по ID",
              status_code=status.HTTP_200_OK, response_model=BlockedUnitSchemaResponse)
async def partial_blocked_unit(request: BlockedUnitsSchemaPartialRequest, blocked_unit_id: int,
                               session: AsyncSession = Depends(get_session)):
    service = BlockedUnitsService(session)
    updated_unit = await service.partial_update_blocked_unit(request, blocked_unit_id)
    return updated_unit


@router.delete("/blockedUnits/{blocked_unit_id}", summary="Удаление ресурса по ID",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_blocked_units(blocked_unit_id: int, session: AsyncSession = Depends(get_session)):
    service = BlockedUnitsService(session)

    await service.delete_blocked_unit(blocked_unit_id)

