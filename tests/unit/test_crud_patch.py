import pytest
from .test_config import (
    client,
    get_entity_id,
    submenu_other_prefix,
    menu_other_prefix,
    dish_other_prefix,
)


@pytest.mark.order(4)
class TestGroup:
    @pytest.mark.asyncio
    async def test_menu_patch(self):
        menu_id = await get_entity_id('menu_id')
        test_update_entity = {
            'title': 'Updated test menu 1',
            'description': 'Updated description test menu 1'
        }
        response = client.patch(
            menu_other_prefix % {'menu_id': menu_id},
            json=test_update_entity
        )
        assert response.status_code == 200
        assert response.json() == {
            'title': 'Updated test menu 1',
            'description': 'Updated description test menu 1'
        }

    @pytest.mark.asyncio
    async def test_submenu_patch(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        test_update_entity = {
            'title': 'Updated test submenu 1',
            'description': 'Updated description test submenu 1'
        }
        response = client.patch(
            submenu_other_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id
            },
            json=test_update_entity
        )
        assert response.status_code == 200
        assert response.json() == {
            'title': 'Updated test submenu 1',
            'description': 'Updated description test submenu 1',
        }

    @pytest.mark.asyncio
    async def test_dish_patch(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        dish_id = await get_entity_id('dish_id')
        test_update_entity = {
            'title': 'Updated test dish 1',
            'description': 'Updated description test dish 1',
            'price': '14.50'
        }
        response = client.patch(
            dish_other_prefix % {
                'menu_id': menu_id,
                'submenu_id': submenu_id,
                'dish_id': dish_id
            },
            json=test_update_entity
        )
        assert response.status_code == 200
        assert response.json() == {
            'title': 'Updated test dish 1',
            'description': 'Updated description test dish 1',
            'price': '14.50'
        }
