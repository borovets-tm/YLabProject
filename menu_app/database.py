"""Модуль инициализации базы данных и сеанса работы с БД."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from menu_app.config import config

Base = declarative_base()
async_engine = create_async_engine(config.async_sqlalchemy_url)


async def get_db():
    """
    Функция инициализирует сеанса базы данных и возвращает его в виде \
    генератора, пока приложение работает.

    :return: Экземпляр сеанса базы данных.
    """
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
