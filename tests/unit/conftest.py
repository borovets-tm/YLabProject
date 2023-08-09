import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from menu_app.config import config
from menu_app.database import Base, get_db
from menu_app.main import app


def get_connection_string(driver: str = 'asyncpg') -> str:
    return (
        f'postgresql+{driver}://{config.POSTGRES_USER}:'
        f'{config.POSTGRES_PASSWORD}@{config.TEST_HOST_DB}:'
        f'{config.PORT}/{config.TEST_DB}'
    )


async_engine = create_async_engine(
    url=get_connection_string(),
)

OverrideBase = declarative_base()


async def override_get_db():
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


@pytest.fixture(scope='session')
async def async_client() -> AsyncClient:
    return AsyncClient(app=app, base_url='http://localhost')


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


app.dependency_overrides[get_db] = override_get_db
