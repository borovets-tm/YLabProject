"""Сервисный слой приложения, не связанного с конкретной моделью приложения."""
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.repositories.app_repository import get_tree_menu_repository
from menu_app.services.base_service import BaseService


class AppService(BaseService):
    """Класс сервисных методов приложения, не связанных с конкретной \
    моделью."""

    async def get_full_menu(self, db: AsyncSession) -> Sequence:
        """
        Метод обрабатывает запрос на получения всех данных из БД в виде \
        дерева JSON. Проверяет наличие кэша и, при его отсутствии, запишет кэш.

        :param db: Экземпляр сеанса базы данных.
        :return: Древовидное меню со всеми элементами БД.
        """
        cache = await self.get_cache(self.full_menu)
        if cache:
            return cache
        result = await get_tree_menu_repository(db)
        await self.set_cache(self.full_menu, result)
        return result


service: AppService = AppService()
