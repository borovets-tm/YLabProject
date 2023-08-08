from abc import ABC, abstractmethod
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession


class Database(ABC):
    def __init__(self):
        self.async_sessionmaker = None

    async def __call__(self) -> AsyncIterator[AsyncSession]:

        async with self.async_sessionmaker() as session:
            yield session

    @abstractmethod
    def setup(self) -> None:
        ...
