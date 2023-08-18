"""Модуль базовой конфигурации всех тестов."""
from uuid import UUID

from httpx import AsyncClient, Response

from menu_app.main import app, router


class TestReverseClient:
    """Класс формирует работу клиента по CRUD операциям для тестов.\
    Также здесь внедрен метод - аналог reverse из Django."""

    def __init__(self):
        """
        Инициализируется асинхронный клиент и роутер для тестов.
        """
        self.client = AsyncClient(app=app, base_url='http://localhost')
        self.routers = router

    async def reverse(self, url_name: str, **url_path) -> str:
        """
        Метод - аналог Django reverse, получающий путь по имени endpoint и \
        параметрам пути в виде kwargs.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param url_path: kwargs-параметры пути.
        :return: Полный адрес вызываемого endpoint.
        """
        return self.routers.url_path_for(url_name, **url_path)

    async def get(self, url_name: str, **url_path) -> Response:
        """
        Базовый метод get для всех текстов, в которых используется получение\
        объекта или списка объектов.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        url = await self.reverse(url_name, **url_path)
        return await self.client.get(url)

    async def post(self, url_name: str, data: dict, **url_path) -> Response:
        """
        Базовый метод post для всех тестов, в которых используется создание\
        новых сущностей в базе данных.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param data: словарь с данными для создания сущности.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        url = await self.reverse(url_name, **url_path)
        return await self.client.post(url, json=data)

    async def patch(self, url_name: str, data: dict, **url_path):
        """
        Базовый метод post для всех тестов, в которых используется обновление\
        существующих сущностей в базе данных.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param data: словарь с данными для обновления сущности.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        url = await self.reverse(url_name, **url_path)
        return await self.client.patch(url, json=data)

    async def delete(self, url_name: str, **url_path):
        """
        Базовый метод get для всех текстов, в которых используется удаление\
        сущности из базы данных.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        url = await self.reverse(url_name, **url_path)
        return await self.client.delete(url)


class BaseTest:
    """Базовый класс тестов CRUD, в котором хранятся основные свойства и \
    методы, используемые в тестах."""

    menu_id: UUID | None = None
    submenu_id: UUID | None = None
    dish_id: UUID | None = None
    title_menu: str = 'Test menu 1'
    description_menu: str = 'Description test menu 1'
    title_submenu: str = 'Test submenu 1'
    description_submenu: str = 'Description test submenu 1'
    title_dish: str = 'Test dish 1'
    description_dish: str = 'Description test dish 1'
    price_dish: str = '12.53'
    update_title_menu = 'Updated test menu 1'
    update_description_menu = 'Updated description test menu 1'
    update_title_submenu = 'Updated test submenu 1'
    update_description_submenu = (
        'Updated description test submenu 1'
    )
    update_title_dish = 'Updated test dish 1'
    update_description_dish = 'Updated description test dish 1'
    update_price_dish = '14.59'

    def __init__(self):
        """Инициализация клиента для тестов и значений количественного типа."""
        self.client = TestReverseClient()
        self.submenus_count = 0
        self.dishes_count = 0

    @classmethod
    async def set_id(
            cls,
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None
    ) -> None:
        """
        Метод устанавливает значения id для сущностей всех моделей, \
        используемых в тестах.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор под-меню.
        :param dish_id: Идентификатор блюда.
        :return: None.
        """
        if menu_id:
            cls.menu_id = menu_id
        if submenu_id:
            cls.submenu_id = submenu_id
        if dish_id:
            cls.dish_id = dish_id

    async def create_test(
            self,
            url_name: str,
            data: dict,
            **url_path
    ) -> Response:
        """
        Метод, используемый в конфигураторах тестов моделей при создании \
        сущностей, возвращает ответ на запрос для дальнейшего тестирования.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param data: словарь с данными для обновления сущности.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        return await self.client.post(url_name, data, **url_path)

    async def retrieve_test(self, url_name: str, **url_path) -> Response:
        """
        Метод, используемый в конфигураторах тестов моделей при получении \
        сущностей или списка, возвращает ответ на запрос для дальнейшего \
        тестирования.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        return await self.client.get(url_name=url_name, **url_path)

    async def update_test(
            self,
            url_name: str,
            data: dict,
            **url_path
    ) -> Response:
        """
        Метод, используемый в конфигураторах тестов моделей при обновлении \
        сущностей, возвращает ответ на запрос для дальнейшего тестирования.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param data: словарь с данными для обновления сущности.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        return await self.client.patch(url_name, data, **url_path)

    async def delete_test(self, url_name: str, **url_path) -> Response:
        """
        Метод, используемый в конфигураторах тестов моделей при удалении \
        сущностей, возвращает ответ на запрос для дальнейшего тестирования.

        :param url_name: Имя endpoint, указанное в декораторе endpoint.
        :param url_path: kwargs-параметры пути.
        :return: Ответ на запрос.
        """
        return await self.client.delete(url_name=url_name, **url_path)
