"""В модуле реализовано конфигурирование и взаимодействие с базой данных."""
from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()
POSTGRES_USER: str = getenv('POSTGRES_USER', 'default')
POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD')
POSTGRES_DB: str = getenv('POSTGRES_DB')
PORT: str = getenv('PORT')
HOST_DB: str = getenv('HOST_DB')

SQLALCHEMY_URL: str = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{HOST_DB}:{PORT}/{POSTGRES_DB}'
)

engine: Engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> None:
    """
    Генератор сессии взаимодействия с базой данных.

    :return: None.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
