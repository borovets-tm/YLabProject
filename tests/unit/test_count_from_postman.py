"""Модуль количественных тестов, аналогичных тестам из Postman."""
import pytest
from httpx import Response

from .config_test.config_dish import BaseTestDish


@pytest.mark.order(4)
@pytest.mark.asyncio
class TestCountFromPostman:
    """Класс асинхронного тестирования, запускающийся четвертым по списку."""
    base = BaseTestDish()

    async def test_create_menu(self) -> None:
        """
        Создание меню.

        :return: None.
        """
        response: Response = await self.base.menu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_create_submenu(self) -> None:
        """
        Создание под-меню. Увеличение счетчика количества под-меню.

        :return: None.
        """
        response: Response = await self.base.submenu_test_create()
        self.base.check_data_menu['submenus_count'] += 1
        assert response.status_code == 201
        assert response.json() == self.base.check_data_submenu

    async def test_get_empty_list_dish(self) -> None:
        """
        Проверка списка блюда на предмет пустого списка.

        :return: None.
        """
        response: Response = await self.base.dish_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_dish(self) -> None:
        """
        Создание блюда. Увеличение счетчика блюд.

        :return: None.
        """
        response: Response = await self.base.dish_test_create()
        assert response.status_code == 201
        self.base.check_data_menu['dishes_count'] += 1
        self.base.check_data_submenu['dishes_count'] += 1
        assert response.json() == self.base.check_data_dish

    async def test_get_menu_after_created_entities(self) -> None:
        """
        Проверка ответа на запрос конкретного меню после создания сущностей.

        :return: None.
        """
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_menu

    async def test_get_submenu_after_created_entities(self) -> None:
        """
        Проверка ответа на запрос конкретного под-меню после создания \
        сущностей.

        :return: None.
        """
        response: Response = await self.base.submenu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_submenu

    async def test_delete_submenu(self) -> None:
        """
        Удаление под-меню. Уменьшение счетчиков.

        :return: None.
        """
        response: Response = await self.base.submenu_test_delete()
        assert response.status_code == 200
        self.base.check_data_menu['submenus_count'] -= 1
        self.base.check_data_menu['dishes_count'] -= 1
        self.base.check_data_submenu['dishes_count'] -= 1
        assert response.json() == self.base.successful_delete_submenu

    async def test_not_found_submenu(self) -> None:
        """
        Проверка на отсутствие конкретного под-меню после удаления.

        :return: None.
        """
        response: Response = await self.base.submenu_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_submenu

    async def test_get_list_dish_is_empty(self) -> None:
        """
        Проверка на признак пустого списка блюд после удаления под-меню.

        :return: None.
        """
        response: Response = await self.base.dish_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_menu_after_delete_submenu(self) -> None:
        """
        Получение конкретного меню после удаление под-меню. \
        Проверка на соответствие данных после удаление сущностей.

        :return: None.
        """
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_menu

    async def test_remove_menu(self) -> None:
        """
        Удаление меню. Проверка ответа на успешность удаления.

        :return: None.
        """
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu

    async def test_get_empty_list_menu(self) -> None:
        """
        Проверка списка меню на признак чистого списка.

        :return: None.
        """
        response: Response = await self.base.menu_test_get_list()
        assert response.status_code == 200
        assert response.json() == []
