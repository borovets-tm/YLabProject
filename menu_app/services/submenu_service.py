"""Модуль сервисного слоя для модели Submenu."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.repositories.submenu_repository import SubmenuRepository, repository
from menu_app.schemas.submenu import Submenu, SubmenuCreate

from .base_service import BaseService


class SubmenuService(BaseService):
    """Модель сервисных методов для подменю."""

    def __init__(self) -> None:
        """Инициализация класса с указанием слоя репозитория."""
        super().__init__()
        self.repository: SubmenuRepository = repository

    async def get_list(self, db: AsyncSession) -> list[Submenu]:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка подменю, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :return: Список подменю.
        """
        result = await self.get_cache('submenu.get_list')
        if not result:
            result = await self.repository.get_list(db)
            await self.set_cache('submenu.get_list', result)
        return result

    async def get(self, db: AsyncSession, submenu_id: UUID) -> Submenu:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра подменю, устанавливает кэш и передает данные в\
        роутер.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор подменю.
        :return: Экземпляр модели.
        """
        result = await self.get_cache(f'submenu.get.{submenu_id}')
        if not result:
            result = await self.repository.get(db, submenu_id)
            await self.set_cache(f'submenu.get.{submenu_id}', result)
        return result

    async def create(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            menu_id: UUID
    ) -> Submenu:
        """
        Метод работает с методом создания нового экземпляра подменю, удаляя из\
        кэша записи результатов запросов: получения списков меню, подменю;\
        информации о меню, связанного с подменю.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для создания нового экземпляра.
        :param menu_id: Идентификатор меню.
        :return: Экземпляр созданного подменю.
        """
        await self.delete_cache(
            [
                'menu.get_list',
                f'menu.get{menu_id}',
                'submenu.get_list'
            ]
        )
        return await self.repository.create(db, data, menu_id)

    async def update(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            submenu_id: UUID
    ) -> Submenu:
        """
        Метод удаляет из кэша записи запросов списка подменю и обновляемого\
        подменю.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для обновления.
        :param submenu_id: Идентификатор подменю.
        :return: Экземпляр подменю с обновленными данными.
        """
        await self.delete_cache(
            [
                'submenu.get_list',
                f'submenu.get.{submenu_id}'
            ]
        )
        result = await self.repository.update(db, data, submenu_id)
        return result

    async def delete(
            self,
            db: AsyncSession,
            submenu_id: UUID
    ) -> JSONResponse:
        """
        Метод удаляет весь кэш при удалении подменю. Удаление всего кэша\
        обусловлено тем, что удаление отдельных сегментов увеличит нагрузку\
        на запрос.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор удаляемого подменю.
        :return: Ответ об успехе или неудачи удаления.
        """
        await self.flush_redis()
        result = await self.repository.remove(db, submenu_id)
        return result


service: SubmenuService = SubmenuService()
