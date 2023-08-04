from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.schemas.dish import DishCreate, Dish
from menu_app.repositories.dish_repository import (
    repository,
    DishRepository
)
from .config import set_cache, get_cache, delete_cache, flush_redis


class DishService:

    def __init__(self):
        self.repository: DishRepository = repository

    async def get_list(self, db: Session) -> List[Dish]:
        result = await get_cache('dish.get_list')
        if not result:
            result = await self.repository.get_list(db)
            await set_cache('dish.get_list', result)
        return result

    async def get(self, db: Session, dish_id: UUID) -> Dish:
        result = await get_cache(f'dish.get.{dish_id}')
        if not result:
            result = await self.repository.get(db, dish_id)
            await set_cache(f'dish.get.{dish_id}', result)
        return result

    async def create(
            self,
            db: Session,
            data: DishCreate,
            submenu_id: UUID,
            menu_id: UUID,
    ) -> Dish:
        await delete_cache(
            [
                'menu.get_list',
                f'menu.get{menu_id}',
                'submenu.get_list',
                f'submenu.get{submenu_id}',
                'dish.get_list'
            ]
        )
        return await self.repository.create(db, data, submenu_id)

    async def update(
            self,
            db: Session,
            data: DishCreate,
            dish_id: UUID
    ) -> Dish:
        await delete_cache(['dish.get_list', f'dish.get.{dish_id}'])
        result = await self.repository.update(db, data, dish_id)
        return result

    async def delete(
            self,
            db: Session,
            submenu_id: UUID,
    ) -> JSONResponse:
        await flush_redis()
        result = await self.repository.remove(db, submenu_id)
        return result


service = DishService()
