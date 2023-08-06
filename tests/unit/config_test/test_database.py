"""В модуле реализовано конфигурирование и взаимодействие с базой данных."""
from os import getenv
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from menu_app.database import get_db
from menu_app.main import app

load_dotenv()
POSTGRES_USER: str | None = getenv('POSTGRES_USER', 'default')
POSTGRES_PASSWORD: str | None = getenv('POSTGRES_PASSWORD')
PORT: str | None = getenv('PORT')
HOST_DB: str | None = getenv('HOST_DB')
USED_DB: str | None = getenv('TEST_DB')

SQLALCHEMY_URL: str = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{HOST_DB}:{PORT}/{USED_DB}'
)

engine: Engine = create_engine(SQLALCHEMY_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator:
    """
    Генератор тестовой сессии взаимодействия с базой данных.

    :return: Экземпляром сеанса базы данных.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
