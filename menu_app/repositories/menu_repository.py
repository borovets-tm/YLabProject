"""Модуль реализует функционал запросов к базе данных модели Menu по CRUD."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import RowMapping, Sequence, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce
from starlette.responses import JSONResponse

from menu_app.models import Menu, Submenu
from menu_app.repositories.base_repository import BaseRepository
from menu_app.schemas.menu_schemas import MenuCreate


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
        subquery = (
            select(
                Submenu.menu_id,
                Submenu.id.label('submenu_id'),
                func.count(Submenu.dishes).label('dishes_count')
            )
            .outerjoin(Submenu.dishes)
            .group_by(Submenu.id)
            .subquery('subquery')
        )
        query = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(subquery.c.submenu_id).label('submenus_count'),
                func.sum(
                    coalesce(subquery.c.dishes_count, 0)
                ).label('dishes_count')
            )
            .outerjoin(
                subquery, self.model.id == subquery.c.menu_id
            )
            .group_by(self.model.id)
        )
        result = await db.stream(query)
        curr = await result.mappings().all()
        return curr

    async def get(self, db: AsyncSession, menu_id: UUID) -> RowMapping:
        """
        Метод получения конкретного меню.

        :param db: Экземпляром сеанса базы данных.
        :param menu_id: Идентификатор меню.
        :return: Меню с указанным идентификатором.
        """
        subquery = (
            select(
                Submenu.menu_id,
                Submenu.id.label('submenu_id'),
                func.count(Submenu.dishes).label('dishes_count')
            )
            .outerjoin(Submenu.dishes)
            .filter(Submenu.menu_id == menu_id)
            .group_by(Submenu.menu_id, Submenu.id)
            .subquery('subquery')
        )
        query = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(subquery.c.submenu_id).label('submenus_count'),
                func.sum(
                    coalesce(subquery.c.dishes_count, 0)
                ).label('dishes_count')
            )
            .outerjoin(
                subquery, self.model.id == subquery.c.menu_id
            )
            .filter(self.model.id == menu_id)
            .group_by(self.model.id)
        )
        result = await db.stream(query)
        curr = await result.mappings().first()
        if curr:
            return curr
        raise HTTPException(status_code=404, detail='menu not found')

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
        query = (
            select(self.model)
            .filter(self.model.id == menu_id)
        )
        result = await db.stream(query)
        menu = await result.scalars().first()
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
            await db.stream(query)
            await db.commit()
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
