from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from auth.services import AuthService
from db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import Token, UserCreate, User
from starlette import status
from auth.security import decode_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.post('/login', response_model=Token, summary="Авторизация пользователя", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    auth_service = AuthService(session)

    user = await auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens = await auth_service.create_access_token_service(user)

    return tokens


@router.post('/register', response_model=User, summary="Регистрация пользователя",
             status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    auth_service = AuthService(session)

    db_user = await auth_service.create_user(user)
    return db_user


@router.post('/token/refresh', response_model=Token, summary="Обновление токенов", status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str, session: AsyncSession = Depends(get_session)):
    auth_service = AuthService(session)
    payload = decode_access_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user = await auth_service.auth_repository.get_user_by_login(payload['sub'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    tokens = await auth_service.create_access_token_service(user)
    return tokens
