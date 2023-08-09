import pytest

from menu_app.database import Base

from .conftest import async_engine


@pytest.mark.order('last')
@pytest.mark.asyncio
async def test_drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
