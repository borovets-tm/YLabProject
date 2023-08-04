"""Модуль используется для инициализации методов кэширования в слое."""
import pickle
from os import getenv
from typing import Any

import aioredis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST: str = getenv('REDIS_HOST', 'localhost')

url_redis: str = f'redis://{REDIS_HOST}/1'


async def set_cache(request: str, response: Any) -> None:
    """
    Функция задает значение кэша с ключом request и значением результата\
    запроса.

    :param request: Ключ запроса.
    :param response: Ответ, полученный на запрос от базы данных.
    :return: None.
    """
    response = pickle.dumps(response)
    async with aioredis.from_url(url_redis, decode_responses=True) as redis:
        await redis.set(request, response)


async def get_cache(request: str) -> Any:
    """
    Функция получает из кэша значение запроса к базе данных.

    :param request: Ключ запроса.
    :return: Декодированные данные.
    """
    async with aioredis.from_url(url_redis, decode_responses=True) as redis:
        cache = await redis.get(request)
    if cache:
        cache = pickle.loads(cache)
    return cache


async def delete_cache(request: list[str]) -> None:
    """
    Функция удаляет записи кэша всех передаваемых ключей.

    :param request: Список ключей запроса для удаления.
    :return:None.
    """
    async with aioredis.from_url(url_redis, decode_responses=True) as redis:
        await redis.delete(*request)


async def flush_redis() -> None:
    """
    Очищает весь кэш из redis.

    :return: None.
    """
    async with aioredis.from_url(url_redis) as redis:
        await redis.flushdb(asynchronous=True)
