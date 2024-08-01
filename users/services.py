from sqlalchemy.ext.asyncio import AsyncSession
from users.repositories.users_repository import UsersRepository
from fastapi import HTTPException
from starlette import status
from users.schemas import UsersSchemaRequest, UsersSchemaRequestPartial
from permissions.permission_verification import PermissionVerification


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UsersRepository(db)
        self.permission_verification = PermissionVerification(db)

    async def get_users(self, current_user: dict):
        if self.permission_verification.get_verification(current_user['permissions']):
            return await self.user_repository.get_users()

    async def get_user(self, user_id: int, current_user: dict):
        if self.permission_verification.get_verification(current_user['permissions']):
            user = await self.user_repository.get_user_by_id(user_id)

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            return user

    async def update_user(self, request: UsersSchemaRequest, user_id: int, current_user: dict):
        if self.permission_verification.put_patch_verification(current_user['permissions']):
            existing_user = await self.user_repository.get_user_by_id(user_id)

            if existing_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            existing_user.job_number = request.job_number
            existing_user.first_name = request.first_name
            existing_user.last_name = request.last_name

            return await self.user_repository.update_user(existing_user)

    async def partial_update_user(self, request: UsersSchemaRequestPartial, user_id: int, current_user: dict):
        if self.permission_verification.put_patch_verification(current_user['permissions']):
            existing_user = await self.user_repository.get_user_by_id(user_id)

            if existing_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            if request.first_name:
                existing_user.first_name = request.first_name

            if request.last_name:
                existing_user.last_name = request.last_name

            if request.job_number:
                existing_user.job_number = request.job_number

            return await self.user_repository.update_user(existing_user)

    async def delete_user(self, user_id: int, current_user: dict):
        if self.permission_verification.delete_verification(current_user['permissions']):
            existing_user = await self.user_repository.get_user_by_id(user_id)

            if existing_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            await self.user_repository.delete_user(existing_user)
