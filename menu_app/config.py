"""Модуль хранит базовые переменные для работы приложения."""
from abc import ABC
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):
    """Переменные полученные из env файла для работы приложения."""

    POSTGRES_USER: str | None = getenv('POSTGRES_USER', 'default')
    POSTGRES_PASSWORD: str | None = getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT: str | None = getenv('POSTGRES_PORT')
    POSTGRES_HOST: str | None = getenv('POSTGRES_HOST')
    POSTGRES_DB: str | None = getenv('POSTGRES_DB')
    TEST_DB: str | None = getenv('TEST_DB')
    TEST_HOST_DB: str | None = getenv('TEST_HOST_DB')
    REDIS_HOST: str | None = getenv('REDIS_HOST')
    RABBITMQ_DEFAULT_USER: str | None = getenv('RABBITMQ_DEFAULT_USER')
    RABBITMQ_DEFAULT_PASS: str | None = getenv('RABBITMQ_DEFAULT_PASS')
    RABBITMQ_HOST: str | None = getenv('RABBITMQ_HOST')
    BASE_DIR = Path(__file__).resolve().parent.parent
    async_sqlalchemy_url: str = (
        f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
        f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    sync_sqlalchemy_url: str = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
        f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    broker_url = (
        f'pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}'
        f'@{RABBITMQ_HOST}//'
    )
    url_redis = f'redis://{REDIS_HOST}'


config = Config()
