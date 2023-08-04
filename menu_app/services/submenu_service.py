"""Модуль сервисного слоя для модели Submenu."""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.schemas.submenu import SubmenuCreate, Submenu
from menu_app.repositories.submenu_repository import (
    repository,
    SubmenuRepository
)
from .config import set_cache, get_cache, delete_cache, flush_redis


class SubmenuService:
    """Модель сервисных методов для подменю."""

    def __init__(self):
        """Инициализация класса с указанием слоя репозитория."""
        self.repository: SubmenuRepository = repository

    async def get_list(self, db: Session) -> List[Submenu]:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка подменю, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :return: Список подменю.
        """
        result = await get_cache('submenu.get_list')
        if not result:
            result = await self.repository.get_list(db)
            await set_cache('submenu.get_list', result)
        return result

    async def get(self, db: Session, submenu_id: UUID) -> Submenu:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра подменю, устанавливает кэш и передает данные в\
        роутер.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор подменю.
        :return: Экземпляр модели.
        """
        result = await get_cache(f'submenu.get.{submenu_id}')
        if not result:
            result = await self.repository.get(db, submenu_id)
            await set_cache(f'submenu.get.{submenu_id}', result)
        return result

    async def create(
            self,
            db: Session,
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
        await delete_cache(
            [
                'menu.get_list',
                f'menu.get{menu_id}',
                'submenu.get_list'
            ]
        )
        return await self.repository.create(db, data, menu_id)

    async def update(
            self,
            db: Session,
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
        await delete_cache(['submenu.get_list', f'submenu.get.{submenu_id}'])
        result = await self.repository.update(db, data, submenu_id)
        return result

    async def delete(
            self,
            db: Session,
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
        await flush_redis()
        result = await self.repository.remove(db, submenu_id)
        return result


service: SubmenuService = SubmenuService()
