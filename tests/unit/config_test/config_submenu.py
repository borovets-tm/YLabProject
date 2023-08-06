from .config_menu import BaseTestMenu


class BaseTestSubmenu(BaseTestMenu):

    def __init__(self):
        super().__init__()
        self.check_data_submenu = {
            'id': self.submenu_id,
            'title': self.title_submenu,
            'description': self.description_submenu,
            'dishes_count': self.dishes_count
        }
        self.update_check_data_submenu = {
            'title': self.update_title_submenu,
            'description': self.update_description_submenu,
        }
        self.successful_delete_submenu = {
            'message': 'The submenu has been deleted'
        }
        self.not_found_submenu = {'detail': 'submenu not found'}

    async def submenu_test_create(self):
        test_entity = {
            'title': self.title_submenu,
            'description': self.description_submenu
        }
        response = await self.create_test(
            'create_submenu',
            data=test_entity,
            menu_id=self.menu_id
        )
        submenu_id = response.json()['id']
        await self.set_id(submenu_id=submenu_id)
        self.check_data_submenu['id'] = submenu_id
        return response

    async def submenu_test_get_list(self):
        return await self.retrieve_test(
            'get_list_submenu',
            menu_id=self.menu_id
        )

    async def submenu_test_get(self):
        return await self.retrieve_test(
            'get_submenu',
            menu_id=self.menu_id,
            submenu_id=self.submenu_id
        )

    async def submenu_test_update(self):
        test_update_entity = {
            'title': self.update_title_submenu,
            'description': self.update_description_submenu
        }
        return await self.update_test(
            'update_submenu',
            data=test_update_entity,
            menu_id=self.menu_id,
            submenu_id=self.submenu_id
        )

    async def submenu_test_delete(self):
        return await self.delete_test(
            'delete_submenu',
            menu_id=self.menu_id,
            submenu_id=self.submenu_id
        )
