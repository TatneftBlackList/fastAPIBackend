from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from logs.schemas import LogsSchema
from logs.services import UserRequestLogService
from db.session import get_session
from auth.dependencies import get_current_user

router = APIRouter()


@router.get("/logs", response_model=List[LogsSchema], status_code=status.HTTP_200_OK,
            summary="Возвращает массив логгов")
async def get_all_logs(current_user: Annotated[dict, Depends(get_current_user)],
                       session: AsyncSession = Depends(get_session)):
    service = UserRequestLogService(session)

    logs = await service.get_logs(current_user)

    return logs


@router.get("/logs/{log_id}", response_model=LogsSchema, status_code=status.HTTP_200_OK,
            summary="Возвращает лог по ID")
async def get_log(log_id: int,
                  current_user: Annotated[dict, Depends(get_current_user)],
                  session: AsyncSession = Depends(get_session)):
    service = UserRequestLogService(session)

    log = await service.get_log(current_user, log_id)
    return log
