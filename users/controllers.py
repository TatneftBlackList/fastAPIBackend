from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from starlette import status

from auth.dependencies import get_current_user
from db.session import get_session
from users.schemas import UsersSchemaResponse, UsersSchemaRequest, UsersSchemaRequestPartial
from users.services import UserService

router = APIRouter()


@router.get("/users", response_model=List[UsersSchemaResponse],
            summary="Возвращает массив пользователей", status_code=status.HTTP_200_OK)
async def get_users(current_user: Annotated[dict, Depends(get_current_user)],
                    session: AsyncSession = Depends(get_session)):
    service = UserService(session)

    users = await service.get_users()
    return users


@router.get("/users/{user_id}", response_model=UsersSchemaResponse,
            summary="Возвращает пользователя по ID", status_code=status.HTTP_200_OK)
async def get_user(user_id: int,
                   current_user: Annotated[dict, Depends(get_current_user)],
                   session: AsyncSession = Depends(get_session)):
    service = UserService(session)

    user = await service.get_user(user_id)
    return user


@router.put("/users/{user_id}", response_model=UsersSchemaResponse,
            summary="Полное обновление ресурса по ID", status_code=status.HTTP_200_OK)
async def update_user(user_id: int,
                      request: UsersSchemaRequest,
                      current_user: Annotated[dict, Depends(get_current_user)],
                      session: AsyncSession = Depends(get_session)):
    service = UserService(session)

    user = await service.update_user(request, user_id)
    return user


@router.patch("/users/{user_id}", response_model=UsersSchemaResponse,
              summary="Частичное обновление ресурса по ID", status_code=status.HTTP_200_OK)
async def partial_update_user(user_id: int,
                              request: UsersSchemaRequestPartial,
                              current_user: Annotated[dict, Depends(get_current_user)],
                              session: AsyncSession = Depends(get_session)):
    service = UserService(session)

    user = await service.partial_update_user(request, user_id)
    return user


@router.delete("/users/{user_id}", summary="Удаление русурса по ID", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      current_user: Annotated[dict, Depends(get_current_user)],
                      session: AsyncSession = Depends(get_session)):
    service = UserService(session)

    await service.delete_user(user_id)
