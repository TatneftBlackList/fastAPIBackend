from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from auth.controllers import router as auth_router
from roles.controllers import router as roles_router
from company.controllers import router as company_router
from permissions.controllers import router as permissions_router
from users.controllers import router as users_router
from blocked_units.controllers import router as blocked_units_router
from db.seed_roles import seed_roles
from db.seed_permissions import seed_permissions
from db.session import async_session_maker


async def on_startup():
    from company.models import CompanyModel
    from blocked_units.models.blocked_units import BlockedUnitsModel
    from blocked_units.models.passports import PassportsModel
    from auth.models import AuthModel
    from roles.models import RolesModel
    from permissions.models import PermissionModel
    from users.models.users import UserModel
    from users.models.users_permission import UserPermissionModel

    app.include_router(auth_router, prefix="/api/v1", tags=['Авторизация и регистрация'])
    app.include_router(roles_router, prefix="/api/v1", tags=['Роли'])
    app.include_router(company_router, prefix="/api/v1", tags=['CRUD по компаниям'])
    app.include_router(permissions_router, prefix="/api/v1", tags=['Permissions для пользователей'])
    app.include_router(users_router, prefix="/api/v1", tags=['CRUD по пользователям'])
    app.include_router(blocked_units_router, prefix="/api/v1", tags=['CRUD по заблокированным пользователям'])

    async with async_session_maker() as session:
        await seed_roles(session)
        await seed_permissions(session)


app = FastAPI(on_startup=[on_startup])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
