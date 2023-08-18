"""Модуль тестирования CRUD для меню."""
import pytest
from httpx import Response

from .config_test.config_menu import BaseTestMenu


@pytest.mark.order(1)
@pytest.mark.asyncio
class TestCRUDMenu:
    """Класс асинхронного тестирования, запускаемый первым по порядку."""
    base = BaseTestMenu()

    async def test_get_empty_list_menu(self) -> None:
        """
        Проверка отсутствия сущностей меню в базе данных перед созданием \
        сущности.

        :return: None.
        """
        response: Response = await self.base.menu_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_menu(self) -> None:
        """
        Создание меню.

        :return: None.
        """
        response: Response = await self.base.menu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_get_menu(self) -> None:
        """
        Получение конкретного меню после создания.

        :return: None.
        """
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_menu

    async def test_update_menu(self) -> None:
        """
        Обновление конкретного меню.

        :return: None.
        """
        response: Response = await self.base.menu_test_update()
        assert response.status_code == 200
        assert response.json() == self.base.update_check_data_menu

    async def test_delete_menu(self) -> None:
        """
        Удаление меню.

        :return: None.
        """
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu

    async def test_not_found_menu(self) -> None:
        """
        Проверка отсутствия конкретного меню в базе данных после удаления.

        :return: None.
        """
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_menu
