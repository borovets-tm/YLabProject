import pytest

from .test_config import (
    client,
    dish_other_prefix,
    get_entity_id,
    menu_other_prefix,
    submenu_other_prefix,
)


@pytest.mark.order(5)
class TestGroup:
    @pytest.mark.asyncio
    async def test_dish_remove(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        dish_id = await get_entity_id('dish_id')
        response = client.delete(
            dish_other_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id,
                'dish_id': dish_id
            }
        )
        assert response.status_code == 200
        assert response.json() == {
            'message': 'The dish has been deleted'
        }

    @pytest.mark.asyncio
    async def test_submenu_remove(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.delete(
            submenu_other_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id
            }
        )
        assert response.status_code == 200
        assert response.json() == {
            'message': 'The submenu has been deleted'
        }

    @pytest.mark.asyncio
    async def test_menu_remove(self):
        menu_id = await get_entity_id('menu_id')
        response = client.delete(menu_other_prefix % {'menu_id': menu_id})
        assert response.status_code == 200
        assert response.json() == {
            'message': 'The menu has been deleted'
        }
