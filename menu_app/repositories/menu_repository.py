"""Модуль реализует функционал запросов к базе данных модели Menu по CRUD."""
from typing import List, Union
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce
from starlette.responses import JSONResponse

from menu_app.schemas.menu import MenuCreate
from menu_app.models import Menu
from menu_app.models import Submenu
from menu_app.models import Dish
from .config import data_commit, get_entity, remove_entity


class MenuRepository:
    """Класс взаимодействия с базой данных для модели Menu с методами CRUD."""

    def __init__(self):
        """Инициализация класса с указанием используемой модели."""
        self.model = Menu

    async def get_list(self, db: Session) -> List[Menu]:
        """
        Метод получения списка меню.

        :param db: Экземпляром сеанса базы данных.
        :return: Список меню.
        """
        submenus = (
            db
            .query(
                Submenu.menu_id,
                func.count(Dish.id).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.menu_id)
            .subquery('submenus')
        )
        result = (
            db
            .query(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(submenus.c.menu_id).label('submenus_count'),
                coalesce(submenus.c.dishes_count, 0).label('dishes_count')
            )
            .outerjoin(
                submenus, self.model.id == submenus.c.menu_id
            )
            .group_by(self.model.id, submenus.c.dishes_count)
            .all()
        )
        return result

    async def get(self, db: Session, menu_id: UUID) -> Menu:
        """
        Метод получения конкретного меню.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :return: Меню с указанным идентификатором.
        """
        subquery = (
            db
            .query(
                Submenu.menu_id,
                func.count(Dish.id).label('dishes_count')
            )
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
            .filter(Submenu.menu_id == menu_id)
            .group_by(Submenu.menu_id)
            .subquery('submenus')
        )
        query = (
            db
            .query(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(subquery.c.menu_id).label('submenus_count'),
                coalesce(subquery.c.dishes_count, 0).label('dishes_count')
            )
            .join(
                subquery, self.model.id == subquery.c.menu_id, isouter=True
            )
            .filter(self.model.id == menu_id)
            .group_by(self.model.id, subquery.c.dishes_count)
            .first()
        )
        if not query:
            raise HTTPException(status_code=404, detail='menu not found')
        return query

    async def create(self, db: Session, data: MenuCreate) -> Menu:
        """
        Метод создания меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные нового меню.
        :return: Информация о созданном меню.
        """
        menu = self.model(
            id=uuid4(),
            title=data.title,
            description=data.description
        )
        try:
            await data_commit(db, menu)
        except Exception as e:
            print(e)
        return menu

    async def update(
            self,
            db: Session,
            data: MenuCreate,
            menu_id: UUID
    ) -> Menu:
        """
        Метод обновления информации о существующем меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Обновляемая информация.
        :param menu_id: Идентификатор меню.
        :return: Обновленная информация о меню.
        """
        menu = await get_entity(db, self.model, menu_id)
        menu.title = data.title
        menu.description = data.description
        await data_commit(db, menu)
        return menu

    async def remove(
            self,
            db: Session,
            menu_id: UUID
    ) -> Union[JSONResponse, HTTPException]:
        """
        Метод удаляет меню из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            await remove_entity(db, self.model, menu_id)
            return JSONResponse(
                status_code=200,
                content={
                    'message': 'The menu has been deleted'
                }
            )
        except Exception as e:
            return HTTPException(
                status_code=404,
                detail=e
            )


repository = MenuRepository()