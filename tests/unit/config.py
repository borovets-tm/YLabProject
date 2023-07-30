from os import getenv
from uuid import UUID

import aioredis
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from menu_app.main import app

client = TestClient(app=app)
load_dotenv()
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
url_redis = f'redis://{REDIS_HOST}'

menu_post_prefix = '/api/v1/menus/'
menu_other_prefix = '/api/v1/menus/%(menu_id)s/'
submenu_post_prefix = '/api/v1/menus/%(menu_id)s/submenus/'
submenu_other_prefix = '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/'
dish_post_prefix = '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/dishes/'
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
