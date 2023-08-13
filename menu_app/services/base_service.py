"""Модуль используется для инициализации методов кэширования в слое."""
import pickle
from typing import Any

import aioredis

from menu_app.config import config


class BaseService:
    """Базовый класс сервисных операций."""

    def __init__(self):
        """Инициализация базовых значений адреса redis и времени жизни кэша."""
        self.url_redis = config.url_redis
        self.cache_lifetime = 15
        self.full_menu = 'get_tree_menu'
        self.get_list_menu = 'get_list.menu'
        self.get_menu = 'get.menu.%(menu_id)s'
        self.get_list_submenu = self.get_list_menu + '.%(menu_id)s.submenu'
        self.get_submenu = self.get_menu + '.submenu.%(submenu_id)s'
        self.get_list_dish = self.get_list_submenu + '.%(submenu_id)s.dish'
        self.get_dish = self.get_submenu + '.dish.%(dish_id)s'

    @classmethod
    async def get_lazy_s(cls, path_params: dict) -> dict:
        """
        Метод собирает словарь из аргументов ленивой строки.

        :param path_params: Параметры пути, адреса запроса.
        :return: словарь с аргументами.
        """
        s = {
            'menu_id': path_params.get('menu_id', ''),
            'submenu_id': path_params.get('submenu_id', ''),
            'dish_id': path_params.get('dish_id', '')
        }
        return s

    async def set_cache(self, request: str, response: Any) -> None:
        """
        Функция задает значение кэша с ключом request и значением результата\
        запроса.

        :param request: Ключ запроса.
        :param response: Ответ, полученный на запрос от базы данных.
        :return: None.
        """
        response = pickle.dumps(response)
        async with aioredis.from_url(self.url_redis) as redis:
            await redis.set(request, response, ex=self.cache_lifetime)

    async def get_cache(self, request: str) -> Any:
        """
        Функция получает из кэша значение запроса к базе данных.

        :param request: Ключ запроса.
        :return: Декодированные данные.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            cache = await redis.get(request)
        if cache:
            cache = pickle.loads(cache)
        return cache

    async def delete_cache(self, request: list[str]) -> None:
        """
        Функция удаляет записи кэша всех передаваемых ключей.

        :param request: Список ключей запроса для удаления.
        :return:None.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            await redis.delete(*request)

    async def get_keys_by_patterns(self, pattern: str) -> list:
        """
        Метод получает список всех ключей кэша, хранящихся в Redis по \
        подстроке.

        :param pattern: Подстрока для поиска.
        :return: Список всех найденных ключей.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            return await redis.keys(pattern)

    async def flush_redis(self) -> None:
        """
        Очищает весь кэш из redis.

        :return: None.
        """
        async with aioredis.from_url(self.url_redis) as redis:
            await redis.flushdb(asynchronous=True)
            await redis.connection_pool.disconnect()
