"""В модуле реализовано конфигурирование и взаимодействие с базой данных."""
from os import getenv
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
TEST: bool = getenv('TEST', '0') == '1'
POSTGRES_USER: str | None = getenv('POSTGRES_USER', 'default')
POSTGRES_PASSWORD: str | None = getenv('POSTGRES_PASSWORD')
PORT: str | None = getenv('PORT')
HOST_DB: str | None = getenv('HOST_DB')
USED_DB: str | None = getenv('TEST_DB') if TEST else getenv('POSTGRES_DB')

SQLALCHEMY_URL: str = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{HOST_DB}:{PORT}/{USED_DB}'
)

engine: Engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """
    Генератор сессии взаимодействия с базой данных.

    :return: Экземпляром сеанса базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
