"""Модуль дополнительной конфигурации тестов CRUD для модели Dish."""
from httpx import Response

from tests.unit.config_test.config_submenu import BaseTestSubmenu


class BaseTestDish(BaseTestSubmenu):
    """Класс тонкого конфигурирования тестов для сущностей модели Dish."""

    def __init__(self):
        """Инициализация контрольных значений."""
        super().__init__()
        self.check_data_dish = {
            'id': self.dish_id,
            'title': self.title_dish,
            'description': self.description_dish,
            'price': self.price_dish
        }
        self.update_check_data_dish = {
            'title': self.update_title_dish,
            'description': self.update_description_dish,
            'price': self.update_price_dish
        }
        self.successful_delete_dish = {'message': 'The dish has been deleted'}
        self.not_found_dish = {'detail': 'dish not found'}

    async def dish_test_create(self) -> Response:
        """
        Метод создания тестового блюда, используемый в тестах для проверки.

        :return: Ответ на запрос.
        """
        test_entity = {
            'title': self.title_dish,
            'description': self.description_dish,
            'price': self.price_dish
        }
        response = await self.create_test(
            'create_dish',
            test_entity,
            menu_id=self.menu_id,
            submenu_id=self.submenu_id
        )
        dish_id = response.json()['id']
        await self.set_id(dish_id=dish_id)
        self.check_data_dish['id'] = dish_id
        return response

    async def dish_test_get_list(self) -> Response:
        """
        Метод запроса списка блюд, используемый в тестах для проверки.

        :return: Ответ на запрос.
        """
        return await self.retrieve_test(
            'get_list_dish',
            menu_id=self.menu_id,
            submenu_id=self.submenu_id
        )

    async def dish_test_get(self) -> Response:
        """
        Метод запроса конкретного блюда по идентификатору, используемый в \
        тестах для проверки.

        :return: Ответ на запрос.
        """
        return await self.retrieve_test(
            'get_dish',
            menu_id=self.menu_id,
            submenu_id=self.submenu_id,
            dish_id=self.dish_id
        )

    async def dish_test_update(self) -> Response:
        """
        Метод обновления блюда, используемый в тестах для проверки.

        :return: Ответ на запрос.
        """
        test_update_entity = {
            'title': self.update_title_dish,
            'description': self.update_description_dish,
            'price': self.update_price_dish
        }
        return await self.update_test(
            'update_dish',
            data=test_update_entity,
            menu_id=self.menu_id,
            submenu_id=self.submenu_id,
            dish_id=self.dish_id
        )

    async def dish_test_delete(self) -> Response:
        """
        Метод удаления блюда, используемый в тестах для проверки.

        :return: Ответ на запрос.
        """
        return await self.delete_test(
            'delete_dish',
            menu_id=self.menu_id,
            submenu_id=self.submenu_id,
            dish_id=self.dish_id
        )
