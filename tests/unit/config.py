import json

import pytest
from fastapi.testclient import TestClient
from menu_app.main import app

client = TestClient(app=app)

menu_post_prefix = '/api/v1/menus/'
menu_other_prefix = '/api/v1/menus/%(menu_id)s/'
submenu_post_prefix = '/api/v1/menus/%(menu_id)s/submenus/'
submenu_other_prefix = '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/'
dish_post_prefix = '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/dishes/'
dish_other_prefix = (
    '/api/v1/menus/%(menu_id)s/submenus/%(submenu_id)s/dishes/%(dish_id)s/'
)


def dump_data(data: dict):
    with open('tests/unit/test_data.json', 'w') as f:
        json.dump(data, f)


def load_data():
    with open('tests/unit/test_data.json', 'r') as f:
        return json.load(f)
