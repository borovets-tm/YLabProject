"""Модуль реализует функционал запросов к базе данных модели Dish по CRUD."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import Row, Sequence, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.models import Dish
from menu_app.schemas.dish import DishCreate

from .base_repository import BaseRepository


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
        async with db as session:
            query = select(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.price
            )
            result = await session.execute(query)
            curr = result.all()
        return curr

    async def get(self, db: AsyncSession, dish_id: UUID) -> Row:
        """
        Метод получения конкретного блюда.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: идентификатор блюда.
        :return: Блюдо с указанным идентификатором.
        """
        async with db as session:
            query = (
                select(
                    self.model.id,
                    self.model.title,
                    self.model.description,
                    self.model.price
                )
                .filter(self.model.id == dish_id)
            )
            result = await session.execute(query)
            curr = result.first()
        if not curr:
            raise HTTPException(status_code=404, detail='dish not found')
        return curr

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
        :param submenu_id: Идентификатор подменю, которому относится блюдо.
        :return: Информация о созданном блюде.
        """
        dish = self.model(
            id=uuid4(),
            title=data.title,
            description=data.description,
            price=data.price,
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
        async with db as session:
            query = (
                select(self.model)
                .filter(self.model.id == dish_id)
            )
            result = await session.execute(query)
            dish = result.scalars().one()
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
            async with db as session:
                await session.execute(query)
                await session.commit()
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
