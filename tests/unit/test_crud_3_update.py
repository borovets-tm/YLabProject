import pytest
from .config import (
    client,
    submenu_other_prefix,
    load_data, menu_other_prefix, dish_other_prefix,
)

test_id: dict = {}


@pytest.mark.asyncio
async def test_menu_update():
    global test_id
    test_id = load_data()
    menu_id = test_id['menu_id']
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
async def test_submenu_update():
    menu_id = test_id['menu_id']
    submenu_id = test_id['submenu_id']
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
async def test_dish_update():
    menu_id = test_id['menu_id']
    submenu_id = test_id['submenu_id']
    dish_id = test_id['dish_id']
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
