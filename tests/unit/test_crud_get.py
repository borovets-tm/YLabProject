import aioredis
import pytest
from .config import (
    client,
    get_entity_id,
    menu_other_prefix,
    submenu_other_prefix,
    dish_other_prefix,
)


@pytest.mark.asyncio
async def test_menu_get():
    menu_id = await get_entity_id('menu_id')
    response = client.get(menu_other_prefix % {'menu_id': menu_id})
    assert response.status_code == 200
    assert response.json() == {
        'id': menu_id,
        'title': 'Test menu 1',
        'description': 'Description test menu 1',
        'submenus_count': 1,
        'dishes_count': 1
    }


@pytest.mark.asyncio
async def test_submenu_get():
    menu_id = await get_entity_id('menu_id')
    submenu_id = await get_entity_id('submenu_id')
    response = client.get(
        submenu_other_prefix % {
            'menu_id': menu_id,
            'submenu_id': submenu_id
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': submenu_id,
        'title': 'Test submenu 1',
        'description': 'Description test submenu 1',
        'dishes_count': 1
    }


@pytest.mark.asyncio
async def test_dish_get():
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
    assert response.status_code == 200
    assert response.json() == {
        'id': dish_id,
        'title': 'Test dish 1',
        'description': 'Description test dish 1',
        'price': '12.50'
    }
