from sqlalchemy.ext.asyncio import AsyncSession
from users.repositories.users_repository import UsersRepository
from fastapi import HTTPException
from starlette import status
from users.schemas import UsersSchemaRequest, UsersSchemaRequestPartial


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UsersRepository(db)

    async def get_users(self):
        return await self.user_repository.get_users()

    async def get_user(self, user_id: int):
        user = await self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def update_user(self, user: UsersSchemaRequest, user_id: int):
        existing_user = await self.user_repository.get_user_by_id(user_id)

        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        existing_user.job_number = user.job_number
        existing_user.first_name = user.first_name
        existing_user.last_name = user.last_name

        return await self.user_repository.update_user(existing_user)

    async def partial_update_user(self, user: UsersSchemaRequestPartial, user_id: int):
        existing_user = await self.user_repository.get_user_by_id(user_id)

        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.first_name:
            existing_user.first_name = user.first_name

        if user.last_name:
            existing_user.last_name = user.last_name

        if user.job_number:
            existing_user.job_number = user.job_number

        return await self.user_repository.update_user(existing_user)

    async def delete_user(self, user_id: int):
        existing_user = await self.user_repository.get_user_by_id(user_id)

        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await self.user_repository.delete_user(existing_user)
