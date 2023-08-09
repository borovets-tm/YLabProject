"""Модуль сервисного слоя для модели Menu."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.repositories.menu_repository import MenuRepository, repository
from menu_app.schemas.menu import Menu, MenuCreate

from .base_service import BaseService


class MenuService(BaseService):
    """Модель сервисных методов для меню."""

    def __init__(self) -> None:
        """Инициализация класса с указанием слоя репозитория."""
        super().__init__()
        self.repository: MenuRepository = repository

    async def get_list(self, db: AsyncSession) -> list[Menu]:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка меню, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :return: Список меню.
        """
        result = await self.get_cache('menu.get_list')
        if not result:
            result = await self.repository.get_list(db)
            await self.set_cache('menu.get_list', result)
        return result

    async def get(self, db: AsyncSession, menu_id: UUID) -> Menu:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра меню, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :return: Экземпляр модели.
        """
        result = await self.get_cache(f'menu.get.{menu_id}')
        if not result:
            result = await self.repository.get(db, menu_id)
            await self.set_cache(f'menu.get.{menu_id}', result)
        return result

    async def create(self, db: AsyncSession, data: MenuCreate) -> Menu:
        """
        Метод работает с методом создания нового экземпляра меню, удаляя из\
        кэша записи результатов запроса получения списка меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для создания нового экземпляра.
        :return: Экземпляр созданного меню.
        """
        await self.delete_cache(['menu.get_list'])
        return await self.repository.create(db, data)

    async def update(
            self,
            db: AsyncSession,
            data: MenuCreate,
            menu_id: UUID
    ) -> Menu:
        """
        Метод удаляет из кэша записи запросов списка меню и обновляемого меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для обновления.
        :param menu_id: Идентификатор меню.
        :return: Экземпляр меню с обновленными данными.
        """
        await self.delete_cache(['menu.get_list', f'menu.get.{menu_id}'])
        return await self.repository.update(db, data, menu_id)

    async def delete(self, db: AsyncSession, menu_id: UUID) -> JSONResponse:
        """
        Метод удаляет весь кэш при удалении меню. Удаление всего кэша\
        обусловлено тем, что удаление отдельных сегментов увеличит нагрузку\
        на запрос.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор удаляемого меню.
        :return: Ответ об успехе или неудачи удаления.
        """
        delete_list = ['menu.get_list']
        delete_list += await self.get_keys_by_patterns(f'*{menu_id}*')
        await self.delete_cache(delete_list)
        result = await self.repository.remove(db, menu_id)
        return result


service: MenuService = MenuService()
