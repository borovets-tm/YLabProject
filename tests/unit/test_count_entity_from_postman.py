import pytest

from .test_config import (
    app,
    client,
    dish_post_list_prefix,
    get_entity_id,
    menu_other_prefix,
    menu_post_list_prefix,
    set_entity_id,
)


@pytest.mark.order(8)
class TestPostman:
    @pytest.mark.asyncio
    async def test_menu_create(self):
        test_entity = {
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
        response = client.post(
            app.url_path_for('create_menu'),
            json=test_entity
        )
        assert response.status_code == 201
        data = response.json()
        menu_id = data['id']
        await set_entity_id('menu_id', menu_id)
        assert data == {
            'id': menu_id,
            'title': 'My menu 1',
            'description': 'My menu description 1',
            'submenus_count': 0,
            'dishes_count': 0
        }

    @pytest.mark.asyncio
    async def test_submenu_create(self):
        menu_id = await get_entity_id('menu_id')
        test_entity = {
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
            'menu_id': menu_id
        }
        response = client.post(
            app.url_path_for('create_submenu', menu_id=menu_id),
            json=test_entity
        )
        data = response.json()
        submenu_id = data['id']
        await set_entity_id('submenu_id', submenu_id)
        assert response.status_code == 201
        assert data == {
            'id': submenu_id,
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
            'dishes_count': 0
        }

    @pytest.mark.asyncio
    async def test_dish1_create(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        test_entity = {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50',
            'submenu_id': submenu_id
        }
        response = client.post(
            app.url_path_for(
                'create_dish',
                menu_id=menu_id,
                submenu_id=submenu_id
            ),
            json=test_entity
        )
        data = response.json()
        dish_id = data['id']
        await set_entity_id('dish1_id', dish_id)
        assert response.status_code == 201
        assert data == {
            'id': dish_id,
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50'
        }

    @pytest.mark.asyncio
    async def test_dish2_create(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        test_entity = {
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50',
            'submenu_id': submenu_id
        }
        response = client.post(
            app.url_path_for(
                'create_dish',
                menu_id=menu_id,
                submenu_id=submenu_id
            ),
            json=test_entity
        )
        data = response.json()
        dish_id = data['id']
        await set_entity_id('dish2_id', dish_id)
        assert response.status_code == 201
        assert data == {
            'id': dish_id,
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50'
        }

    @pytest.mark.asyncio
    async def test_menu_get_after_created_entities(self):
        menu_id = await get_entity_id('menu_id')
        response = client.get(app.url_path_for('get_menu', menu_id=menu_id))
        assert response.status_code == 200
        assert response.json() == {
            'id': menu_id,
            'title': 'My menu 1',
            'description': 'My menu description 1',
            'submenus_count': 1,
            'dishes_count': 2
        }

    @pytest.mark.asyncio
    async def test_submenu_get_after_created_entities(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.get(
            app.url_path_for(
                'get_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id
            )
        )
        assert response.status_code == 200
        assert response.json() == {
            'id': submenu_id,
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
            'dishes_count': 2
        }

    @pytest.mark.asyncio
    async def test_submenu_remove(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.delete(
            app.url_path_for(
                'delete_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id
            )
        )
        assert response.status_code == 200
        assert response.json() == {
            'message': 'The submenu has been deleted'
        }

    @pytest.mark.asyncio
    async def test_submenu_get_not_found(self):
        menu_id = await get_entity_id('menu_id')
        submenu_id = await get_entity_id('submenu_id')
        response = client.get(
            app.url_path_for(
                'get_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id
            )
        )
        assert response.status_code == 404
        assert response.json() == {
            'detail': 'submenu not found'
        }

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

    @pytest.mark.asyncio
    async def test_menu_get_after_remove_submenu(self):
        menu_id = await get_entity_id('menu_id')
        response = client.get(menu_other_prefix % {'menu_id': menu_id})
        assert response.status_code == 200
        assert response.json() == {
            'id': menu_id,
            'title': 'My menu 1',
            'description': 'My menu description 1',
            'submenus_count': 0,
            'dishes_count': 0
        }

    @pytest.mark.asyncio
    async def test_menu_remove(self):
        menu_id = await get_entity_id('menu_id')
        response = client.delete(menu_other_prefix % {'menu_id': menu_id})
        assert response.status_code == 200
        assert response.json() == {
            'message': 'The menu has been deleted'
        }

    @pytest.mark.asyncio
    async def test_get_empty_menus_list(self):
        response = client.get(
            menu_post_list_prefix
        )
        assert response.status_code == 200
        assert response.json() == []
