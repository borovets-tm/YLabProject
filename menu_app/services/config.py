import pickle
from os import getenv
from typing import Any, List

import aioredis
from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = getenv('REDIS_HOST', 'localhost')

url_redis = f'redis://{REDIS_HOST}/1'


async def set_cache(request: str, response: Any) -> None:
    response = pickle.dumps(response)
    async with aioredis.from_url(url_redis, decode_responses=True) as redis:
        await redis.set(request, response)


async def get_cache(request: str):
    async with aioredis.from_url(url_redis, decode_responses=True) as redis:
        cache = await redis.get(request)
    if cache:
        cache = pickle.loads(cache)
    return cache


async def delete_cache(request: List[str]) -> None:
    async with aioredis.from_url(url_redis, decode_responses=True) as redis:
        await redis.delete(*request)


async def flush_redis():
    async with aioredis.from_url(url_redis) as redis:
        await redis.flushdb(asynchronous=True)
