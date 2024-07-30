from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from permissions.services import PermissionService
from permissions.schemas import PermissionSchema
from typing import List
from db.session import get_session
from starlette import status

router = APIRouter()


@router.get("/permissions", response_model=List[PermissionSchema], status_code=status.HTTP_200_OK,
            summary="Возвращает массив прав для пользователя")
async def get_permissions(session: AsyncSession = Depends(get_session)):
    service = PermissionService(session)

    permissions = await service.get_permissions()

    return permissions
