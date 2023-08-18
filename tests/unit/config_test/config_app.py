"""Модуль конфигурации тестов для endpoint получения древовидного меню."""
from uuid import UUID

from httpx import Response

from tests.unit.config_test.config_dish import BaseTestDish


class BaseTestApp(BaseTestDish):
    """Класс основа тестов для endpoint получения древовидного меню, \
    наследуемый от класса основы тестов для CRUD блюд."""

    def __init__(self):
        """Инициализация класса формирует проверочные данные для теста."""
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

    async def set_menu_id(self, menu_id: UUID | None) -> None:
        """
        Метод устанавливает значение id menu в проверочных данных.

        :param menu_id: Идентификатор меню.
        :return: None.
        """
        self.check_data_app[0]['id'] = menu_id

    async def set_submenu_id(self, submenu_id: UUID | None) -> None:
        """
        Метод устанавливает значение id submenu в проверочных данных.

        :param submenu_id: Идентификатор под-меню.
        :return: None.
        """
        self.check_data_app[0]['submenus'][0]['id'] = submenu_id

    async def set_dish_id(self, dish_id: UUID | None) -> None:
        """
        Метод устанавливает значение id dish в проверочных данных.

        :param dish_id: Идентификатор блюда.
        :return: None.
        """
        self.check_data_app[0]['submenus'][0]['dishes'][0]['id'] = dish_id

    async def app_get_tree_menu(self) -> Response:
        """
        Метод использует один из родительских методов для возвращения ответа \
        на get запрос получения древовидного меню.

        :return: Ответ от тестового клиента на get запрос.
        """
        return await self.retrieve_test('full_menu')
