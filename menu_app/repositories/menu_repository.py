"""Модуль реализует функционал запросов к базе данных модели Menu по CRUD."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import Row, Sequence, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce
from starlette.responses import JSONResponse

from menu_app.models import Dish, Menu, Submenu
from menu_app.schemas.menu import MenuCreate

from .base_repository import BaseRepository


class MenuRepository(BaseRepository):
    """Класс взаимодействия с базой данных для модели Menu с методами CRUD."""

    def __init__(self):
        """Инициализация класса с указанием используемой модели."""
        self.model = Menu

    async def get_list(self, db: AsyncSession) -> Sequence:
        """
        Метод получения списка меню.

        :param db: Экземпляром сеанса базы данных.
        :return: Список меню.
        """
        async with db as session:
            subquery = (
                select(
                    Submenu.menu_id,
                    func.count(Dish.id).label('dishes_count')
                )
                .outerjoin(Dish, Submenu.id == Dish.submenu_id)
                .group_by(Submenu.menu_id)
                .subquery('subquery')
            )
            query = (
                select(
                    self.model.id,
                    self.model.title,
                    self.model.description,
                    func.count(subquery.c.menu_id).label('submenus_count'),
                    coalesce(subquery.c.dishes_count, 0).label('dishes_count')
                )
                .outerjoin(
                    subquery, self.model.id == subquery.c.menu_id
                )
                .group_by(self.model.id, subquery.c.dishes_count)
            )
            result = await session.execute(query)
            curr = result.all()
        return curr

    async def get(self, db: AsyncSession, menu_id: UUID) -> Row:
        """
        Метод получения конкретного меню.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :return: Меню с указанным идентификатором.
        """
        async with db as session:
            subquery = (
                select(
                    Submenu.menu_id,
                    func.count(Dish.id).label('dishes_count')
                )
                .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
                .filter(Submenu.menu_id == menu_id)
                .group_by(Submenu.menu_id)
                .subquery('submenus')
            )
            query = (
                select(
                    self.model.id,
                    self.model.title,
                    self.model.description,
                    func.count(subquery.c.menu_id).label('submenus_count'),
                    coalesce(subquery.c.dishes_count, 0).label('dishes_count')
                )
                .outerjoin(
                    subquery, self.model.id == subquery.c.menu_id
                )
                .filter(self.model.id == menu_id)
                .group_by(self.model.id, subquery.c.dishes_count)
            )
            result = await session.execute(query)
            curr = result.first()
        if not curr:
            raise HTTPException(status_code=404, detail='menu not found')
        return curr

    async def create(self, db: AsyncSession, data: MenuCreate) -> Menu:
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
        await self.data_commit(db, menu)
        return menu

    async def update(
            self,
            db: AsyncSession,
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
        async with db as session:
            query = (
                select(self.model)
                .filter(self.model.id == menu_id)
            )
            result = await session.execute(query)
            menu = result.scalars().one()
            menu.title = data.title
            menu.description = data.description
            await self.data_commit(db, menu)
        return menu

    async def remove(
            self,
            db: AsyncSession,
            menu_id: UUID
    ) -> JSONResponse | HTTPException:
        """
        Метод удаляет меню из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            query = delete(self.model).filter(self.model.id == menu_id)
            async with db as session:
                await session.execute(query)
                await session.commit()
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
