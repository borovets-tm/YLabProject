"""Модуль реализует функционал запросов к базе данных модели Dish по CRUD."""
from typing import List
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.models import Dish
from menu_app.schemas.dish import DishCreate
from .config import remove_entity, data_commit, get_entity


class DishRepository:
    """Класс взаимодействия с базой данных для модели Dish с методами CRUD."""

    def __init__(self) -> None:
        """Инициализация класса с указанием используемой модели."""
        self.model = Dish

    async def get_list(self, db: Session) -> List[Dish]:
        """
        Метод получения списка блюд.

        :param db: Экземпляром сеанса базы данных.
        :return: Список блюд.
        """
        result = db.query(self.model).all()
        return result

    async def get(self, db: Session, dish_id: UUID) -> Dish:
        """
        Метод получения конкретного блюда.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: идентификатор блюда.
        :return: Блюдо с указанным идентификатором.
        """
        result = (
            db
            .query(self.model)
            .filter(self.model.id == dish_id)
            .first()
        )
        if not result:
            raise HTTPException(status_code=404, detail='dish not found')
        return result

    async def create(
            self,
            db: Session,
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
        try:
            await data_commit(db, dish)
        except Exception as e:
            print(e)
        return dish

    async def update(
            self,
            db: Session,
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
        dish = await get_entity(db, self.model, dish_id)
        dish.title = data.title
        dish.description = data.description
        dish.price = data.price
        await data_commit(db, dish)
        return dish

    async def remove(self, db: Session, dish_id: UUID) -> JSONResponse:
        """
        Метод удаляет блюдо из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param dish_id: Идентификатор блюда.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            await remove_entity(db, self.model, dish_id)
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
