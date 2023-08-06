import pytest

from .test_config import app, client, get_entity_id


@pytest.mark.order(3)
class TestGroup:

    @pytest.mark.asyncio
    async def test_menus(self):
        menu_id = await get_entity_id('menu_id')
        response = client.get(app.url_path_for('get_list_menu'))
        assert response.status_code == 200
        assert response.json() == [
            {
                'id': menu_id,
                'title': 'Test menu 1',
                'description': 'Description test menu 1',
                'submenus_count': 1,
                'dishes_count': 1
            }
        ]

    @pytest.mark.asyncio
    async def test_submenus(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.get(
            app.url_path_for('get_list_submenu', menu_id=menu_id)
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                'id': submenu_id,
                'title': 'Test submenu 1',
                'description': 'Description test submenu 1',
                'dishes_count': 1
            }
        ]

    @pytest.mark.asyncio
    async def test_dishes(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        dish_id = await get_entity_id('dish_id')
        response = client.get(
            app.url_path_for(
                'get_list_dish',
                menu_id=menu_id,
                submenu_id=submenu_id
            )
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                'id': dish_id,
                'title': 'Test dish 1',
                'description': 'Description test dish 1',
                'price': '12.50'
            }
        ]
