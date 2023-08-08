from abc import ABC
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):
    POSTGRES_USER: str | None = getenv('POSTGRES_USER', 'default')
    POSTGRES_PASSWORD: str | None = getenv('POSTGRES_PASSWORD')
    PORT: str | None = getenv('PORT')
    HOST_DB: str | None = getenv('HOST_DB')
    POSTGRES_DB: str | None = getenv('POSTGRES_DB')
    TEST_DB: str | None = getenv('TEST_DB')


config = Config()
