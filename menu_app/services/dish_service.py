"""Модуль сервисного слоя для модели Dish."""
from uuid import UUID

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.repositories.dish_repository import DishRepository, repository
from menu_app.schemas.dish import Dish, DishCreate

from .config import BaseService


class DishService(BaseService):
    """Модель сервисных методов для блюд."""

    def __init__(self) -> None:
        """Инициализация класса с указанием слоя репозитория."""
        super().__init__()
        self.repository: DishRepository = repository

    async def get_list(self, db: Session, submenu_id, menu_id) -> list[Dish]:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка блюд, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор связанного подменю.
        :param menu_id: Идентификатор связанного меню.
        :return: Список блюд.
        """
        result = await self.get_cache(
            f'dish.get_list.menu{menu_id}.submenu{submenu_id}'
        )
        if not result:
            result = await self.repository.get_list(db)
            await self.set_cache(
                f'dish.get_list.menu{menu_id}.submenu{submenu_id}',
                result
            )
        return result

    async def get(
            self,
            db: Session,
            dish_id: UUID,
            submenu_id, menu_id
    ) -> Dish:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра блюда, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: Идентификатор блюда.
        :param submenu_id: Идентификатор связанного подменю.
        :param menu_id: Идентификатор связанного меню.
        :return: Экземпляр модели.
        """
        result = await self.get_cache(
            f'dish.get.{dish_id}.menu{menu_id}.submenu{submenu_id}'
        )
        if not result:
            result = await self.repository.get(db, dish_id)
            await self.set_cache(
                f'dish.get.{dish_id}.menu{menu_id}.submenu{submenu_id}',
                result
            )
        return result

    async def create(
            self,
            db: Session,
            data: DishCreate,
            submenu_id: UUID,
            menu_id: UUID,
    ) -> Dish:
        """
        Метод работает с методом создания нового экземпляра блюда, удаляя из\
        кэша записи результатов запросов: получения списков меню, подменю и \
        блюд; информации о меню и подменю, связанных с блюдом.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для создания нового экземпляра.
        :param submenu_id: Идентификатор подменю.
        :param menu_id: Идентификатор меню.
        :return: Экземпляр созданного блюда.
        """
        await self.delete_cache(
            [
                'menu.get_list',
                'submenu.get_list',
                'dish.get_list',
                f'*{submenu_id}*',
                f'*{menu_id}*'
            ]
        )
        return await self.repository.create(db, data, submenu_id)

    async def update(
            self,
            db: Session,
            data: DishCreate,
            dish_id: UUID
    ) -> Dish:
        """
        Метод удаляет из кэша записи запросов списка блюд и обновляемого блюда.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для обновления.
        :param dish_id: Идентификатор блюда.
        :return: Экземпляр блюда с обновленными данными.
        """
        await self.delete_cache(['dish.get_list*', f'*{dish_id}*'])
        result = await self.repository.update(db, data, dish_id)
        return result

    async def delete(
            self,
            db: Session,
            dish_id: UUID,
            submenu_id: UUID,
            menu_id: UUID,
    ) -> JSONResponse:
        """
        Метод удаляет весь кэш при удалении блюда. Удаление всего кэша\
        обусловлено тем, что удаление отдельных сегментов увеличит нагрузку\
        на запрос.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: Идентификатор удаляемого блюда.
        :param submenu_id: Идентификатор связанного подменю.
        :param menu_id: Идентификатор связанного меню.
        :return: Ответ об успехе или неудачи удаления.
        """
        await self.delete_cache([
            'submenu.get_list*'
            'menu.get_list',
            f'*{dish_id}*',
            f'*{submenu_id}*',
            f'*{menu_id}*'
        ])
        result = await self.repository.remove(db, dish_id)
        return result


service: DishService = DishService()
