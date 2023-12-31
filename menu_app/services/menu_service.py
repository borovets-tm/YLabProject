"""Модуль сервисного слоя для модели Menu."""
from uuid import UUID

from sqlalchemy import RowMapping, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from menu_app.repositories.menu_repository import MenuRepository, repository
from menu_app.schemas.menu_schemas import Menu, MenuCreate
from menu_app.services.base_service import BaseService


class MenuService(BaseService):
    """Модель сервисных методов для меню."""

    def __init__(self) -> None:
        """Инициализация класса с указанием слоя репозитория."""
        super().__init__()
        self.repository: MenuRepository = repository

    async def get_list(
            self,
            db: AsyncSession
    ) -> Sequence:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка меню, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :return: Список меню.
        """
        cache = await self.get_cache(self.get_list_menu)
        if cache:
            return cache
        result = await self.repository.get_list(db)
        await self.set_cache(self.get_list_menu, result)
        return result

    async def get(
            self,
            db: AsyncSession,
            menu_id: UUID,
            path_params: dict
    ) -> RowMapping:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра меню, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :param path_params: Словарь со списком параметров пути.
        :return: Экземпляр модели.
        """
        s: dict = await self.get_lazy_s(path_params)
        cache = await self.get_cache(
            self.get_menu % s
        )
        if cache:
            return cache
        result = await self.repository.get(db, menu_id)
        await self.set_cache(self.get_menu % s, result)
        return result

    async def create(
            self,
            db: AsyncSession,
            data: MenuCreate,
            background_tasks: BackgroundTasks
    ) -> Menu:
        """
        Метод работает с методом создания нового экземпляра меню, удаляя из\
        кэша записи результатов запроса получения списка меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для создания нового экземпляра.
        :param background_tasks: Фоновые задачи.
        :return: Экземпляр созданного меню.
        """
        background_tasks.add_task(self.delete_cache, [self.get_list_menu])
        return await self.repository.create(db, data)

    async def update(
            self,
            db: AsyncSession,
            data: MenuCreate,
            menu_id: UUID,
            path_params: dict,
            background_tasks: BackgroundTasks
    ) -> Menu:
        """
        Метод удаляет из кэша записи запросов списка меню и обновляемого меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для обновления.
        :param menu_id: Идентификатор меню.
        :param path_params: Словарь со списком параметров пути.
        :param background_tasks: Фоновые задачи.
        :return: Экземпляр меню с обновленными данными.
        """
        s: dict = await self.get_lazy_s(path_params)
        background_tasks.add_task(
            self.delete_cache,
            [self.get_list_menu, self.get_menu % s]
        )
        return await self.repository.update(db, data, menu_id)

    async def delete(
            self,
            db: AsyncSession,
            menu_id: UUID,
            background_tasks: BackgroundTasks
    ) -> JSONResponse:
        """
        Метод удаляет кэш при удалении меню и возвращает ответ пользователю \
        об успехе или неудачи удаления.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор удаляемого меню.
        :param background_tasks: Фоновые задачи.
        :return: Ответ об успехе или неудачи удаления.
        """
        delete_list = [self.get_list_menu]
        delete_list += await self.get_keys_by_patterns(f'*{menu_id}*')
        background_tasks.add_task(self.delete_cache, delete_list)
        result = await self.repository.remove(db, menu_id)
        return result


service: MenuService = MenuService()
