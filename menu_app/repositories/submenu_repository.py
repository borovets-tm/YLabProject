"""Модуль реализует функционал запросов к базе данных модели Submenu по\
CRUD."""
from typing import List
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.models import Submenu
from menu_app.schemas.submenu import SubmenuCreate
from .config import data_commit, get_entity, remove_entity


class SubmenuRepository:
    """Класс взаимодействия с базой данных для модели Submenu с методами\
    CRUD."""

    def __init__(self):
        """Инициализация класса с указанием используемой модели."""
        self.model = Submenu

    async def get_list(self, db: Session) -> List[Submenu]:
        """
        Метод получения списка подменю.

        :param db: Экземпляром сеанса базы данных.
        :return: Список подменю.
        """
        query = (
            db
            .query(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(self.model.dishes).label('dishes_count')
            )
            .outerjoin(self.model.dishes)
            .group_by(self.model.id)
            .all()
        )
        return query

    async def get(self, db: Session, submenu_id: UUID) -> Submenu:
        """
        Метод получения конкретного подменю.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор подменю.
        :return: Подменю с указанным идентификатором.
        """
        result = (
            db
            .query(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(self.model.dishes).label('dishes_count')
            )
            .join(self.model.dishes, isouter=True)
            .filter(self.model.id == submenu_id)
            .group_by(self.model.id)
            .first()
        )
        if not result:
            raise HTTPException(status_code=404, detail='submenu not found')
        return result

    async def create(
            self,
            db: Session,
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
        try:
            await data_commit(db, submenu)
        except Exception as e:
            print(e)
        return submenu

    async def update(
            self,
            db: Session,
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
        submenu = await get_entity(db, self.model, submenu_id)
        submenu.title = data.title
        submenu.description = data.description
        await data_commit(db, submenu)
        return submenu

    async def remove(self, db: Session, submenu_id: UUID) -> JSONResponse:
        """
        Метод удаляет подменю из базы данных.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор подменю.
        :return: JSONResponse об успехе или неудачи удаления.
        """
        try:
            await remove_entity(db, self.model, submenu_id)
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
