import pytest

from .config_test.config_dish import BaseTestDish


@pytest.mark.order(3)
@pytest.mark.asyncio
class TestCRUDSubmenu:
    base = BaseTestDish()

    async def test_create_menu(self) -> None:
        response = await self.base.menu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_create_submenu(self) -> None:
        response = await self.base.submenu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_submenu

    async def test_get_empty_list_dish(self) -> None:
        response = await self.base.dish_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_dish(self) -> None:
        response = await self.base.dish_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_dish

    async def test_get_dish(self) -> None:
        response = await self.base.dish_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_dish

    async def test_update_dish(self) -> None:
        response = await self.base.dish_test_update()
        assert response.status_code == 200
        assert response.json() == self.base.update_check_data_dish

    async def test_delete_dish(self) -> None:
        response = await self.base.dish_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_dish

    async def test_not_found_dish(self) -> None:
        response = await self.base.dish_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_dish

    async def test_delete_menu(self) -> None:
        response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu
