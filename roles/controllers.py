from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user
from db.session import get_session
from starlette import status

from roles.schemas import RolesSchemas
from roles.services import RolesService

router = APIRouter()


@router.get('/roles', status_code=status.HTTP_200_OK, response_model=List[RolesSchemas],
            summary='Возвращает массив ролей')
async def get_roles(current_user: Annotated[dict, Depends(get_current_user)],
                    session: AsyncSession = Depends(get_session)):
    service = RolesService(session)

    roles = await service.get_all_roles()

    return roles

