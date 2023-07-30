import pytest
from .config import (
    client,
    dish_post_prefix,
    menu_post_prefix,
    submenu_post_prefix,
    dump_data,
)


test_id: dict = {}


@pytest.mark.asyncio
async def test_menu_create():
    test_entity = {
        'title': 'Test menu 1',
        'description': 'Description test menu 1'
    }
    response = client.post(menu_post_prefix, json=test_entity)
    assert response.status_code == 201
    data = response.json()
    global test_id
    test_id['menu_id'] = data['id']
    assert data == {
        'id': test_id['menu_id'],
        'title': 'Test menu 1',
        'description': 'Description test menu 1',
        'submenus_count': 0,
        'dishes_count': 0
    }


@pytest.mark.asyncio
async def test_submenu_create():
    global test_id
    menu_id = test_id['menu_id']
    test_entity = {
        'title': 'Test submenu 1',
        'description': 'Description test submenu 1',
        'menu_id': menu_id
    }
    response = client.post(
        submenu_post_prefix % {'menu_id': menu_id},
        json=test_entity
    )
    data = response.json()
    test_id['submenu_id'] = data['id']
    assert response.status_code == 201
    assert data == {
        'id': test_id['submenu_id'],
        'title': 'Test submenu 1',
        'description': 'Description test submenu 1',
        'dishes_count': 0
    }


@pytest.mark.asyncio
async def test_dish_create():
    global test_id
    menu_id = test_id['menu_id']
    submenu_id = test_id['submenu_id']
    test_entity = {
            'title': 'Test dish 1',
            'description': 'Description test dish 1',
            'price': '12.50',
            'submenu_id': submenu_id
        }
    response = client.post(
        dish_post_prefix % {
            'menu_id': menu_id,
            'submenu_id': submenu_id
        },
        json=test_entity
    )
    data = response.json()
    test_id['dish_id'] = data['id']
    assert response.status_code == 201
    assert data == {
        'id': test_id['dish_id'],
        'title': 'Test dish 1',
        'description': 'Description test dish 1',
        'price': '12.50'
    }
    dump_data(test_id)
