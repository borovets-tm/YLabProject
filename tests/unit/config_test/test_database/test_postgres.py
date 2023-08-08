from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from menu_app.config import config
from menu_app.database.postgres import db
from menu_app.main import app

from .test_base import Database


def get_connection_string(driver: str = 'asyncpg') -> str:
    sqlalchemy_url: str = (
        f'postgresql+{driver}://{config.POSTGRES_USER}:'
        f'{config.POSTGRES_PASSWORD}@{config.HOST_DB}:'
        f'{config.PORT}/{config.TEST_DB}'
    )
    return sqlalchemy_url


async_engine = create_async_engine(get_connection_string())

Base = declarative_base()


class PostgresDatabase(Database):
    def setup(self) -> None:
        self.async_sessionmaker: AsyncSession = sessionmaker(
            async_engine,
            class_=AsyncSession
        )


override_db = PostgresDatabase()

app.dependency_overrides[db] = override_db
