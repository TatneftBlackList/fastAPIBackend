from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from db.session import get_session
from auth.services import AuthService
from auth.schemas import TokenData
from auth.models import AuthModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> (
        AuthModel):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    auth_service = AuthService(session)
    user = await auth_service.auth_repository.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
