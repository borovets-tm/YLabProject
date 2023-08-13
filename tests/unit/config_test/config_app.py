from tests.unit.config_test.config_dish import BaseTestDish


class BaseTestApp(BaseTestDish):

    def __init__(self):
        super().__init__()
        self.check_data_app = [
            {
                'id': None,
                'title': self.title_menu,
                'description': self.description_menu,
                'submenus': [
                    {
                        'id': None,
                        'title': self.title_submenu,
                        'description': self.description_submenu,
                        'dishes': [
                            {
                                'id': None,
                                'title': self.title_dish,
                                'description': self.description_dish,
                                'price': self.price_dish
                            }
                        ]
                    }
                ]
            }
        ]

    async def set_menu_id(self, menu_id):
        self.check_data_app[0]['id'] = menu_id

    async def set_submenu_id(self, submenu_id):
        self.check_data_app[0]['submenus'][0]['id'] = submenu_id

    async def set_dish_id(self, dish_id):
        self.check_data_app[0]['submenus'][0]['dishes'][0]['id'] = dish_id

    async def app_get_tree_menu(self):
        return await self.retrieve_test('full_menu')
