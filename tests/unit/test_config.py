from os import getenv
from uuid import UUID

import aioredis
import dotenv
import pytest
from fastapi.testclient import TestClient

from menu_app.main import app

client = TestClient(app=app)
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
url_redis = f'redis://{REDIS_HOST}/2'

menu_post_list_prefix = '/api/v1/menus/'
menu_other_prefix = '/api/v1/menus/%(menu_id)s/'
submenu_post_list_prefix = '/api/v1/menus/%(menu_id)s/submenus/'
submenu_other_prefix = '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/'
dish_post_list_prefix = (
    '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/dishes/'
)
dish_other_prefix = (
    '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/dishes/%(dish_id)s/'
)


async def set_entity_id(key: str, value: UUID):
    redis = await aioredis.from_url(url_redis, decode_responses=True)
    await redis.set(key, value)
    await redis.connection_pool.disconnect()


async def get_entity_id(key: str) -> UUID:
    redis = await aioredis.from_url(url_redis, decode_responses=True)
    entity_id = await redis.get(key)
    await redis.connection_pool.disconnect()
    return entity_id


@pytest.mark.order(0)
@pytest.mark.asyncio
async def test_change_db_on_test():
    dotenv.set_key(dotenv_file, 'TEST', '1')
    test_value = dotenv.get_key(dotenv_file, 'TEST')
    assert test_value == '1'


@pytest.mark.order('last')
@pytest.mark.asyncio
async def test_clear_cache_after_test():
    redis = await aioredis.from_url(url_redis)
    await redis.flushall(asynchronous=True)
    keys = await redis.keys()
    await redis.connection_pool.disconnect()
    assert keys == []
    dotenv.set_key(dotenv_file, 'TEST', '0')
    test_value = dotenv.get_key(dotenv_file, 'TEST')
    assert test_value == '0'
