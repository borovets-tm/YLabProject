import pytest
from httpx import Response

from .config_test.config_dish import BaseTestDish


@pytest.mark.order(4)
@pytest.mark.asyncio
class TestCountFromPostman:
    base = BaseTestDish()

    async def test_create_menu(self) -> None:
        response: Response = await self.base.menu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_create_submenu(self) -> None:
        response: Response = await self.base.submenu_test_create()
        self.base.check_data_menu['submenus_count'] += 1
        assert response.status_code == 201
        assert response.json() == self.base.check_data_submenu

    async def test_get_empty_list_dish(self) -> None:
        response: Response = await self.base.dish_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_dish(self) -> None:
        response: Response = await self.base.dish_test_create()
        assert response.status_code == 201
        self.base.check_data_menu['dishes_count'] += 1
        self.base.check_data_submenu['dishes_count'] += 1
        assert response.json() == self.base.check_data_dish

    async def test_get_menu_after_created_entities(self) -> None:
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_menu

    async def test_get_submenu_after_created_entities(self) -> None:
        response: Response = await self.base.submenu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_submenu

    async def test_delete_submenu(self) -> None:
        response: Response = await self.base.submenu_test_delete()
        assert response.status_code == 200
        self.base.check_data_menu['submenus_count'] -= 1
        self.base.check_data_menu['dishes_count'] -= 1
        self.base.check_data_submenu['dishes_count'] -= 1
        assert response.json() == self.base.successful_delete_submenu

    async def test_not_found_submenu(self) -> None:
        response: Response = await self.base.submenu_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_submenu

    async def test_get_list_dish_is_empty(self) -> None:
        response: Response = await self.base.dish_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_menu_after_delete_submenu(self) -> None:
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_menu

    async def test_remove_menu(self) -> None:
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu

    async def test_get_empty_list_menu(self) -> None:
        response: Response = await self.base.menu_test_get_list()
        assert response.status_code == 200
        assert response.json() == []
