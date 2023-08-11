"""Модуль хранит базовые переменные для работы приложения."""
from abc import ABC
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):
    """Переменные полученные из env файла для работы приложения."""

    POSTGRES_USER: str | None = getenv('POSTGRES_USER', 'default')
    POSTGRES_PASSWORD: str | None = getenv('POSTGRES_PASSWORD')
    PORT: str | None = getenv('PORT')
    HOST_DB: str | None = getenv('HOST_DB')
    POSTGRES_DB: str | None = getenv('POSTGRES_DB')
    TEST_DB: str | None = getenv('TEST_DB')
    TEST_HOST_DB: str | None = getenv('TEST_HOST_DB')
    REDIS_HOST: str | None = getenv('REDIS_HOST')


config = Config()
