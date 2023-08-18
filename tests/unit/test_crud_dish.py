"""Модуль тестирования CRUD для блюд."""
import pytest
from httpx import Response

from .config_test.config_dish import BaseTestDish


@pytest.mark.order(3)
@pytest.mark.asyncio
class TestCRUDDish:
    """Класс асинхронного тестирования, запускаемый третьим по порядку."""
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
        Создание под-меню.

        :return: None.
        """
        response: Response = await self.base.submenu_test_create()
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
        Создание блюда.

        :return: None.
        """
        response: Response = await self.base.dish_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_dish

    async def test_get_dish(self) -> None:
        """
        Получение конкретного блюда.

        :return: None.
        """
        response: Response = await self.base.dish_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_dish

    async def test_update_dish(self) -> None:
        """
        Обновление блюда.

        :return: None.
        """
        response: Response = await self.base.dish_test_update()
        assert response.status_code == 200
        assert response.json() == self.base.update_check_data_dish

    async def test_delete_dish(self) -> None:
        """
        Удаление блюда.

        :return: None.
        """
        response: Response = await self.base.dish_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_dish

    async def test_not_found_dish(self) -> None:
        """
        Проверка отсутствия конкретного блюда после удаления.

        :return: None.
        """
        response: Response = await self.base.dish_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_dish

    async def test_delete_menu(self) -> None:
        """
        Удаление меню после тестов.

        :return: None.
        """
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu
