from typing import List
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.models import Dish
from menu_app.schemas.dish import DishCreate
from .config import remove_entity, data_commit, get_entity


class DishRepository:

    def __init__(self):
        self.model = Dish

    async def get_list(self, db: Session) -> List[Dish]:
        result = db.query(self.model).all()
        return result

    async def get(self, db: Session, dish_id: UUID) -> Dish:
        result = (
            db
            .query(self.model)
            .filter(self.model.id == dish_id)
            .first()
        )
        if not result:
            raise HTTPException(status_code=404, detail='dish not found')
        return result

    async def create(self, db: Session, data: DishCreate, submenu_id: UUID) -> Dish:
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

    async def update(self, db: Session, data: DishCreate, dish_id: UUID) -> Dish:
        dish = await get_entity(db, self.model, dish_id)
        dish.title = data.title
        dish.description = data.description
        dish.price = data.price
        await data_commit(db, dish)
        return dish

    async def remove(self, db: Session, dish_id: UUID) -> JSONResponse:
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


repository = DishRepository()
