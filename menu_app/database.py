from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from menu_app.config import config


def get_connection_string(driver: str = 'asyncpg') -> str:
    sqlalchemy_url: str = (
        f'postgresql+{driver}://{config.POSTGRES_USER}:'
        f'{config.POSTGRES_PASSWORD}@{config.HOST_DB}:'
        f'{config.PORT}/{config.POSTGRES_DB}'
    )
    return sqlalchemy_url


Base = declarative_base()
async_engine = create_async_engine(get_connection_string())


async def get_db():
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()
