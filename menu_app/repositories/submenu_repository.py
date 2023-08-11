"""Модуль реализует функционал запросов к базе данных модели Submenu по\
CRUD."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import RowMapping, Sequence, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.models import Submenu
from menu_app.repositories.base_repository import BaseRepository
from menu_app.schemas.submenu_schemas import SubmenuCreate


class SubmenuRepository(BaseRepository):
    """Класс взаимодействия с базой данных для модели Submenu с методами\
    CRUD."""

    def __init__(self):
        """Инициализация класса с указанием используемой модели."""
        self.model = Submenu

    async def get_list(self, db: AsyncSession) -> Sequence:
        """
        Метод получения списка под-меню.

        :param db: Экземпляром сеанса базы данных.
        :return: Список под-меню.
        """
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
        result = await db.stream(query)
        curr = await result.mappings().all()
        return curr

    async def get(self, db: AsyncSession, submenu_id: UUID) -> RowMapping:
        """
        Метод получения конкретного под-меню.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор под-меню.
        :return: Подменю с указанным идентификатором.
        """
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
        result = await db.stream(query)
        curr = await result.mappings().first()
        if curr:
            return curr
        raise HTTPException(status_code=404, detail='submenu not found')

    async def create(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            menu_id: UUID
    ) -> Submenu:
        """
        Метод создания под-меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные нового под-меню.
        :param menu_id: Идентификатор меню, которому относится под-меню.
        :return: Информация о созданном под-меню.
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
        Метод обновления информации о существующем под-меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Обновляемая информация.
        :param submenu_id: Идентификатор под-меню.
        :return: Обновленная информация под-меню.
        """
        query = (
            select(self.model)
            .filter(self.model.id == submenu_id)
        )
        result = await db.stream(query)
        submenu = await result.scalars().first()
        submenu.title = data.title
        submenu.description = data.description
        await self.data_commit(db, submenu)
        return submenu

    async def remove(self, db: AsyncSession, submenu_id: UUID) -> JSONResponse:
        """
        Метод удаляет под-меню из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор под-меню.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            query = delete(self.model).filter(self.model.id == submenu_id)
            await db.stream(query)
            await db.commit()
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
