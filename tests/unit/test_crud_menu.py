import pytest
from httpx import Response

from .config_test.config_menu import BaseTestMenu


@pytest.mark.order(1)
@pytest.mark.asyncio
class TestCRUDMenu:
    base = BaseTestMenu()

    async def test_get_empty_list_menu(self) -> None:
        response: Response = await self.base.menu_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_menu(self) -> None:
        response: Response = await self.base.menu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_get_menu(self) -> None:
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_menu

    async def test_update_menu(self) -> None:
        response: Response = await self.base.menu_test_update()
        assert response.status_code == 200
        assert response.json() == self.base.update_check_data_menu

    async def test_delete_menu(self) -> None:
        response: Response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu

    async def test_not_found_menu(self) -> None:
        response: Response = await self.base.menu_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_menu
