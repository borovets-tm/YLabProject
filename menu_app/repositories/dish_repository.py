"""Модуль реализует функционал запросов к базе данных модели Dish по CRUD."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import RowMapping, Sequence, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.models import Dish
from menu_app.repositories.base_repository import BaseRepository
from menu_app.schemas.dish_schemas import DishCreate


class DishRepository(BaseRepository):
    """Класс взаимодействия с базой данных для модели Dish с методами CRUD."""

    def __init__(self) -> None:
        """Инициализация класса с указанием используемой модели."""
        self.model = Dish

    async def get_list(self, db: AsyncSession) -> Sequence:
        """
        Метод получения списка блюд.

        :param db: Экземпляром сеанса базы данных.
        :return: Список блюд.
        """
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.round(self.model.current_price, 2).label('price')
        )
        result = await db.stream(query)
        curr = await result.mappings().all()
        return curr

    async def get(self, db: AsyncSession, dish_id: UUID) -> RowMapping:
        """
        Метод получения конкретного блюда.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: идентификатор блюда.
        :return: Блюдо с указанным идентификатором.
        """
        query = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.round(self.model.current_price, 2).label('price')
            )
            .filter(self.model.id == dish_id)
        )
        result = await db.stream(query)
        curr = await result.mappings().first()
        if curr:
            return curr
        raise HTTPException(status_code=404, detail='dish not found')

    async def create(
            self,
            db: AsyncSession,
            data: DishCreate,
            submenu_id: UUID
    ) -> Dish:
        """
        Метод создания блюда.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные нового блюда.
        :param submenu_id: Идентификатор под-меню, которому относится блюдо.
        :return: Информация о созданном блюде.
        """
        dish = self.model(
            id=uuid4(),
            title=data.title,
            description=data.description,
            price=data.price,
            discount=0,
            submenu_id=submenu_id
        )
        await self.data_commit(db, dish)
        return dish

    async def update(
            self,
            db: AsyncSession,
            data: DishCreate,
            dish_id: UUID
    ) -> Dish:
        """
        Метод обновления информации о существующем блюде.

        :param db: Экземпляром сеанса базы данных.
        :param data: Обновляемая информация.
        :param dish_id: Идентификатор блюда.
        :return: Обновленная информация о блюде.
        """
        query = (
            select(self.model)
            .filter(self.model.id == dish_id)
        )
        result = await db.stream(query)
        dish = await result.scalars().first()
        dish.title = data.title
        dish.description = data.description
        dish.price = data.price
        await self.data_commit(db, dish)
        return dish

    async def remove(self, db: AsyncSession, dish_id: UUID) -> JSONResponse:
        """
        Метод удаляет блюдо из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: Идентификатор блюда.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            query = delete(self.model).filter(self.model.id == dish_id)
            await db.stream(query)
            await db.commit()
            return JSONResponse(
                status_code=200,
                content={
                    'message': 'The dish has been deleted'
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=404,
                content={
                    'message': e
                }
            )


repository: DishRepository = DishRepository()
