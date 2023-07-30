import pytest

from .config import (
    load_data,
    client,
    dish_other_prefix,
    submenu_other_prefix,
    menu_other_prefix,
    dump_data,
)

test_id: dict = {}


@pytest.mark.asyncio
async def test_dish_delete():
    global test_id
    test_id = load_data()
    menu_id = test_id['menu_id']
    submenu_id = test_id['submenu_id']
    dish_id = test_id['dish_id']
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
async def test_submenu_delete():
    menu_id = test_id['menu_id']
    submenu_id = test_id['submenu_id']
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
async def test_menu_delete():
    menu_id = test_id['menu_id']
    response = client.delete(menu_other_prefix % {'menu_id': menu_id})
    assert response.status_code == 200
    assert response.json() == {
        'message': 'The menu has been deleted'
    }
    dump_data({})