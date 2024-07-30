from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import settings

engine = create_async_engine(settings.DB_URL)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """

    :return: Возвращает асинхронную сессию
    """
    async with async_session_maker() as session:
        yield session
