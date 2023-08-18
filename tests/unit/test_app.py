"""Модуль тестирования для endpoint получения древовидного меню."""
import pytest
from httpx import Response

from menu_app.services.base_service import BaseService
from tests.unit.config_test.config_app import BaseTestApp


@pytest.mark.order(5)
@pytest.mark.asyncio
class TestGetTreeMenu:
    """Класс асинхронного тестирования, выполняющийся пятым в списке тестов."""
    base = BaseTestApp()

    async def test_create_menu(self) -> None:
        """
        Создание меню и проверка, что меню создано.
        :return: None.
        """
        response: Response = await self.base.menu_test_create()
        await self.base.set_menu_id(self.base.menu_id)
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_create_submenu(self) -> None:
        """
        Создание под-меню и проверка, что под-меню создано.
        :return: None.
        """
        response: Response = await self.base.submenu_test_create()
        await self.base.set_submenu_id(self.base.submenu_id)
        assert response.status_code == 201
        assert response.json() == self.base.check_data_submenu

    async def test_create_dish(self) -> None:
        """
        Создание блюда и проверка, что блюдо создано.
        :return: None.
        """
        response: Response = await self.base.dish_test_create()
        assert response.status_code == 201
        await self.base.set_dish_id(self.base.dish_id)
        assert response.json() == self.base.check_data_dish

    async def test_get_tree_menu(self) -> None:
        """
        Проверка получения древовидного меню и соответствие ответа, требуемым \
        данным.

        :return: None.
        """
        response: Response = await self.base.app_get_tree_menu()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_app

    async def test_remove_menu(self) -> None:
        """
        Удаление меню и связанных элементов. Проверка получения положительного\
         ответа.

        :return: None.
        """
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu

    async def test_get_empty_list_menu(self) -> None:
        """
        Проверка после удаления на признак чистого списка. Используется \
        удаление кэша, т.к. все запросы хранятся в кэше 15 секунд, при этом \
        время выполнения тестов ~1 секунда.

        :return: None.
        """
        await BaseService().flush_redis()
        response: Response = await self.base.app_get_tree_menu()
        assert response.status_code == 200
        assert response.json() == []
