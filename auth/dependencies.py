from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from db.session import get_session
from auth.services import AuthService
from auth.schemas import TokenData
from auth.models import AuthModel
from starlette.requests import Request


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme),
                            session: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: str = payload.get("sub")
        permissions: list = payload.get("permissions", [])
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)

    except JWTError:
        raise credentials_exception

    auth_service = AuthService(session)
    user = await auth_service.auth_repository.get_user_by_login(login=token_data.login)

    if user is None:
        raise credentials_exception

    request.state.user = user

    return {
        "login": login,
        "permissions": permissions
    }
