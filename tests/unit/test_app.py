import pytest
from httpx import Response

from tests.unit.config_test.config_app import BaseTestApp


@pytest.mark.order(5)
@pytest.mark.asyncio
class TestGetTreeMenu:
    base = BaseTestApp()

    async def test_create_menu(self) -> None:
        response: Response = await self.base.menu_test_create()
        await self.base.set_menu_id(self.base.menu_id)
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_create_submenu(self) -> None:
        response: Response = await self.base.submenu_test_create()
        await self.base.set_submenu_id(self.base.submenu_id)
        assert response.status_code == 201
        assert response.json() == self.base.check_data_submenu

    async def test_create_dish(self) -> None:
        response: Response = await self.base.dish_test_create()
        assert response.status_code == 201
        await self.base.set_dish_id(self.base.dish_id)
        assert response.json() == self.base.check_data_dish

    async def test_get_tree_menu(self) -> None:
        response: Response = await self.base.app_get_tree_menu()
        assert response.status_code == 200
        print(response.json())
        print('*' * 20)
        print(self.base.check_data_app)
        assert response.json() == self.base.check_data_app

    async def test_remove_menu(self) -> None:
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu

    async def test_get_empty_list_menu(self) -> None:
        response: Response = await self.base.menu_test_get_list()
        assert response.status_code == 200
        assert response.json() == []
