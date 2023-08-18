"""Модуль инициализации тестов, в котором производятся предварительные \
настройки для работы pytest."""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from menu_app.config import config
from menu_app.database import Base, get_db
from menu_app.main import app

test_sqlalchemy_url: str = (
    f'postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@'
    f'{config.TEST_HOST_DB}:{config.POSTGRES_PORT}/{config.TEST_DB}'
)
async_engine: AsyncEngine = create_async_engine(
    url=test_sqlalchemy_url,
)
OverrideBase: DeclarativeBase = declarative_base()


async def override_get_db() -> AsyncGenerator:
    """
    Функция генерирует экземпляр сеанса базы данных, а также создает таблицы \
    в базе данных при первом обращении.

    :return: Генератор экземпляра сеанса базы данных.
    """
    async_session: sessionmaker = sessionmaker(
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
    """
    Функция создает тестового клиента на уровне фикстур для дальнейшего \
    использования в тестах.

    :return: Асинхронный тестовый клиент.
    """
    return AsyncClient(app=app, base_url='http://localhost')


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """
    Функция генерирует loop для тестов на уровне фикстур.

    :return: Генератор асинхронного loop.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


app.dependency_overrides[get_db] = override_get_db
