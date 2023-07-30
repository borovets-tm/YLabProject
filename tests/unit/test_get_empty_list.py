import pytest
from .test_config import (
    client,
    get_entity_id,
    menu_post_list_prefix,
    dish_post_list_prefix,
    submenu_post_list_prefix,
)


@pytest.mark.order(7)
class TestGroup:
    @pytest.mark.asyncio
    async def test_get_empty_menus_list(self):
        response = client.get(
            menu_post_list_prefix
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_empty_submenus_list(self):
        menu_id = await get_entity_id('menu_id')
        response = client.get(
            submenu_post_list_prefix % {
                'menu_id': menu_id
            }
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_empty_dishes_list(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.get(
            dish_post_list_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id
            }
        )
        assert response.status_code == 200
        assert response.json() == []
