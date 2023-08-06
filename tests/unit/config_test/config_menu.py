from httpx import Response

from .config_base import BaseTest


class BaseTestMenu(BaseTest):

    def __init__(self):
        super().__init__()
        self.check_data_menu = {
            'id': None,
            'title': self.title_menu,
            'description': self.description_menu,
            'submenus_count': self.submenus_count,
            'dishes_count': self.dishes_count
        }
        self.update_check_data_menu = {
            'title': self.update_title_menu,
            'description': self.update_description_menu,
        }
        self.successful_delete_menu = {'message': 'The menu has been deleted'}
        self.not_found_menu = {'detail': 'menu not found'}

    async def menu_test_create(self) -> Response:
        test_entity = {
            'title': self.title_menu,
            'description': self.description_menu
        }
        response: Response = await self.create_test('create_menu', test_entity)
        menu_id = response.json()['id']
        await self.set_id(menu_id=menu_id)
        self.check_data_menu['id'] = menu_id
        return response

    async def menu_test_get_list(self) -> Response:
        return await self.retrieve_test('get_list_menu')

    async def menu_test_get(self) -> Response:
        return await self.retrieve_test('get_menu', menu_id=self.menu_id)

    async def menu_test_update(self) -> Response:
        test_update_entity = {
            'title': self.update_title_menu,
            'description': self.update_description_menu
        }
        return await self.update_test(
            'update_menu',
            data=test_update_entity,
            menu_id=self.menu_id
        )

    async def menu_test_delete(self) -> Response:
        return await self.delete_test('delete_menu', menu_id=self.menu_id)
