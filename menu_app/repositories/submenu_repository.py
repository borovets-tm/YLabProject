"""Модуль реализует функционал запросов к базе данных модели Submenu по\
CRUD."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import Row, Sequence, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.models import Submenu
from menu_app.schemas.submenu import SubmenuCreate

from .base_repository import BaseRepository


class SubmenuRepository(BaseRepository):
    """Класс взаимодействия с базой данных для модели Submenu с методами\
    CRUD."""

    def __init__(self):
        """Инициализация класса с указанием используемой модели."""
        self.model = Submenu

    async def get_list(self, db: AsyncSession) -> Sequence:
        """
        Метод получения списка подменю.

        :param db: Экземпляром сеанса базы данных.
        :return: Список подменю.
        """
        async with db as session:
            query = (
                select(
                    self.model.id,
                    self.model.title,
                    self.model.description,
                    func.count(self.model.dishes).label('dishes_count')
                )
                .outerjoin(self.model.dishes)
                .group_by(self.model.id)
            )
            result = await session.execute(query)
            curr = result.all()
        return curr

    async def get(self, db: AsyncSession, submenu_id: UUID) -> Row:
        """
        Метод получения конкретного подменю.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор подменю.
        :return: Подменю с указанным идентификатором.
        """
        async with db as session:
            query = (
                select(
                    self.model.id,
                    self.model.title,
                    self.model.description,
                    func.count(self.model.dishes).label('dishes_count')
                )
                .outerjoin(self.model.dishes)
                .filter(self.model.id == submenu_id)
                .group_by(self.model.id)
            )
            result = await session.execute(query)
            curr = result.first()
        if not curr:
            raise HTTPException(status_code=404, detail='submenu not found')
        return curr

    async def create(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            menu_id: UUID
    ) -> Submenu:
        """
        Метод создания подменю.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные нового подменю.
        :param menu_id: Идентификатор меню, которому относится подменю.
        :return: Информация о созданном подменю.
        """
        submenu = self.model(
            id=uuid4(),
            title=data.title,
            description=data.description,
            menu_id=menu_id
        )
        await self.data_commit(db, submenu)
        return submenu

    async def update(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            submenu_id: UUID
    ) -> Submenu:
        """
        Метод обновления информации о существующем подменю.

        :param db: Экземпляром сеанса базы данных.
        :param data: Обновляемая информация.
        :param submenu_id: Идентификатор подменю.
        :return: Обновленная информация подменю.
        """
        async with db as session:
            query = (
                select(self.model)
                .filter(self.model.id == submenu_id)
            )
            result = await session.execute(query)
            submenu = result.scalars().one()
            submenu.title = data.title
            submenu.description = data.description
            await self.data_commit(db, submenu)
        return submenu

    async def remove(self, db: AsyncSession, submenu_id: UUID) -> JSONResponse:
        """
        Метод удаляет подменю из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор подменю.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            query = delete(self.model).filter(self.model.id == submenu_id)
            async with db as session:
                await session.execute(query)
                await session.commit()
            return JSONResponse(
                status_code=200,
                content={
                    'message': 'The submenu has been deleted'
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=404,
                content={
                    'message': e
                }
            )


repository = SubmenuRepository()
