from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.repositories import AuthRepository
from auth.schemas import UserCreate
from auth.models import AuthModel
from starlette import status
from auth.security import verify_password, get_password_hash, create_access_token
from users.repositories.users_repository import UsersRepository
from users.repositories.users_permission_repository import UserPermissionRepository
from users.models.users_permission import UserPermissionModel
from users.models.users import UserModel


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.auth_repository = AuthRepository(db)
        self.user_repository = UsersRepository(db)
        self.user_permission_repository = UserPermissionRepository(db)

    async def authenticate_user(self, login: str, password: str):
        user = await self.auth_repository.get_user_by_login(login)

        if not user:
            return False

        if not verify_password(password, user.password):
            return False

        return user

    async def create_access_token_service(self, user: AuthModel):
        token_data = {"sub": user.login}
        return create_access_token(token_data)

    async def create_user(self, user: UserCreate):
        login = await self.auth_repository.get_user_by_login(user.login)

        if login is not None:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Login already registered",
            )

        existing_job_number = await self.user_repository.get_user_by_job_number(user.job_number)

        if existing_job_number is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Job number already registered",
            )

        new_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            job_number=user.job_number
        )
        user_db = await self.user_repository.create_user(new_user)

        for permission in user.permissions_id:
            user_permissions = UserPermissionModel(
                user_id=user_db.id,
                permission_id=permission,
            )
            await self.user_permission_repository.create_permission(user_permissions)

        hashed_password = get_password_hash(user.password)
        db_user = AuthModel(
            login=user.login,
            password=hashed_password,
            role=user.roleID,
            user_id=user_db.id,
        )
        return await self.auth_repository.create_user(db_user)
