from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.repositories import AuthRepository
from auth.schemas import UserCreate
from auth.models import AuthModel
from starlette import status
from auth.security import verify_password, get_password_hash, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.auth_repository = AuthRepository(db)

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
        hashed_password = get_password_hash(user.password)
        db_user = AuthModel(
            login=user.login,
            password=hashed_password,
            role=user.roleID,
        )
        return await self.auth_repository.create_user(db_user)

