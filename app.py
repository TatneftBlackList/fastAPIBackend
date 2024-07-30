from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from auth.controllers import router as auth_router
from roles.controllers import router as roles_router
from company.controllers import router as company_router
from db.seed_roles import seed_roles
from db.session import async_session_maker


async def on_startup():
    from company.models import CompanyModel
    from blocked_units.models.blocked_units import BlockedUnitsModel
    from blocked_units.models.passports import PassportsModel
    from auth.models import AuthModel
    from roles.models import RolesModel

    app.include_router(auth_router, prefix="/api/v1", tags=["Авторизация и регистрация"])
    app.include_router(roles_router, prefix="/api/v1", tags=['Роли'])
    app.include_router(company_router, prefix="/api/v1", tags=['CRUD по компаниям'])

    async with async_session_maker() as session:
        await seed_roles(session)


app = FastAPI(on_startup=[on_startup])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
