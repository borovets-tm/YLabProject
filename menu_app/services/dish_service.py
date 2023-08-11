"""Модуль сервисного слоя для модели Dish."""
from uuid import UUID

from sqlalchemy import RowMapping, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from menu_app.repositories.dish_repository import DishRepository, repository
from menu_app.schemas.dish import Dish, DishCreate

from .base_service import BaseService


class DishService(BaseService):
    """Модель сервисных методов для блюд."""

    def __init__(self) -> None:
        """Инициализация класса с указанием слоя репозитория."""
        super().__init__()
        self.repository: DishRepository = repository

    async def get_list(
            self,
            db: AsyncSession,
            path_params: dict
    ) -> Sequence:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка блюд, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param path_params: Словарь со списком параметров пути.
        :return: Список блюд.
        """
        s: dict = await self.get_lazy_s(path_params)
        cache = await self.get_cache(
            self.get_list_dish % s
        )
        if cache:
            return cache
        result = await self.repository.get_list(db)
        await self.set_cache(self.get_list_dish % s, result)
        return result

    async def get(
            self,
            db: AsyncSession,
            dish_id: UUID,
            path_params: dict
    ) -> RowMapping:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра блюда, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: Идентификатор блюда.
        :param path_params: Словарь со списком параметров пути.
        :return: Экземпляр модели.
        """
        s: dict = await self.get_lazy_s(path_params)
        cache = await self.get_cache(self.get_dish % s)
        if cache:
            return cache
        result = await self.repository.get(db, dish_id)
        await self.set_cache(self.get_dish % s, result)
        return result

    async def create(
            self,
            db: AsyncSession,
            data: DishCreate,
            submenu_id: UUID,
            path_params: dict,
            background_tasks: BackgroundTasks
    ) -> Dish:
        """
        Метод работает с методом создания нового экземпляра блюда, удаляя из\
        кэша записи результатов запросов: получения списков меню, под-меню и \
        блюд; информации о меню и под-меню, связанных с блюдом.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для создания нового экземпляра.
        :param submenu_id: Идентификатор под-меню, к которому относится блюдо.
        :param path_params: Словарь со списком параметров пути.
        :param background_tasks: Фоновые задачи.
        :return: Экземпляр созданного блюда.
        """
        s: dict = await self.get_lazy_s(path_params)
        background_tasks.add_task(
            self.delete_cache,
            [
                self.get_list_menu,
                self.get_menu % s,
                self.get_list_submenu % s,
                self.get_submenu % s,
                self.get_list_dish % s,
            ]
        )
        return await self.repository.create(db, data, submenu_id)

    async def update(
            self,
            db: AsyncSession,
            data: DishCreate,
            dish_id: UUID,
            path_params: dict,
            background_tasks: BackgroundTasks
    ) -> Dish:
        """
        Метод удаляет из кэша записи запросов списка блюд и обновляемого блюда.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для обновления.
        :param dish_id: Идентификатор блюда.
        :param path_params: Словарь со списком параметров пути.
        :param background_tasks: Фоновые задачи.
        :return: Экземпляр блюда с обновленными данными.
        """
        s: dict = await self.get_lazy_s(path_params)
        background_tasks.add_task(
            self.delete_cache,
            [self.get_list_dish % s, self.get_dish % s]
        )
        return await self.repository.update(db, data, dish_id)

    async def delete(
            self,
            db: AsyncSession,
            dish_id: UUID,
            path_params: dict,
            background_tasks: BackgroundTasks
    ) -> JSONResponse:
        """
        Метод удаляет весь кэш при удалении блюда и возвращает ответ \
        пользователю об успехе или неудачи удаления.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: Идентификатор удаляемого блюда.
        :param path_params: Словарь со списком параметров пути.
        :param background_tasks: Фоновые задачи.
        :return: Ответ об успехе или неудачи удаления.
        """
        s: dict = await self.get_lazy_s(path_params)
        delete_list = [
            self.get_list_menu,
            self.get_menu % s,
            self.get_list_submenu % s,
            self.get_submenu % s,
            self.get_list_dish % s
        ]
        delete_list += await self.get_keys_by_patterns(f'*{dish_id}*')
        background_tasks.add_task(self.delete_cache, delete_list)
        result = await self.repository.remove(db, dish_id)
        return result


service: DishService = DishService()
