"""Модуль послетестового выполнения."""
import pytest

from menu_app.database import Base
from menu_app.services.base_service import BaseService

from .conftest import async_engine


@pytest.mark.order('last')
@pytest.mark.asyncio
async def test_drop_db() -> None:
    """
    Удаление таблиц из базы данных и очистка кэша после всех тестов.

    :return: None.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await BaseService().flush_redis()
