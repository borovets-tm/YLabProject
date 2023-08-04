import pytest

from .test_config import (
    client,
    dish_other_prefix,
    get_entity_id,
    menu_other_prefix,
    submenu_other_prefix,
)


@pytest.mark.order(6)
class TestGroup:

    @pytest.mark.asyncio
    async def test_menu_get_not_found(self):
        menu_id = await get_entity_id('menu_id')
        response = client.get(menu_other_prefix % {'menu_id': menu_id})
        assert response.status_code == 404
        assert response.json() == {
            'detail': 'menu not found'
        }

    @pytest.mark.asyncio
    async def test_submenu_get_not_found(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.get(
            submenu_other_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id
            }
        )
        assert response.status_code == 404
        assert response.json() == {
            'detail': 'submenu not found'
        }

    @pytest.mark.asyncio
    async def test_dish_get_not_found(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        dish_id = await get_entity_id('dish_id')
        response = client.get(
            dish_other_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id,
                'dish_id': dish_id
            }
        )
        assert response.status_code == 404
        assert response.json() == {
            'detail': 'dish not found'
        }
