from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session, async_session_maker
from logs.models import UserRequestLogModel


class UserRequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = Response("Internal server error", status_code=500)
        try:
            async with async_session_maker() as session:
                request.state.session = session

                if not hasattr(request.state, 'user'):
                    request.state.user = None
                response = await call_next(request)

                user_id = request.state.user.id if request.state.user else None
                if user_id is not None:
                    log_entry = UserRequestLogModel(
                        user_id=user_id,
                        path=request.url.path,
                        method=request.method,
                        response_status=response.status_code
                    )
                    session.add(log_entry)
                    await session.commit()
                else:
                    pass
        except Exception as e:
            print(f"Request failed: {e}")
        return response
