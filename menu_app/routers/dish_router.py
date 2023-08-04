from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.dish import DishCreate, Dish
from menu_app.services.dish_service import service

routers = APIRouter(prefix='/{submenu_id}/dishes')


@routers.get(
    '/',
    tags=['dishes'],
    summary='Получаем список блюд',
    response_model=List[Dish]
)
async def get_list(db: Session = Depends(get_db)) -> List[Dish]:
    return await service.get_list(db)


@routers.get(
    '/{dish_id}/',
    summary='Получаем блюдо',
    tags=['dishes'],
    response_model=Dish
)
async def get(dish_id: UUID, db: Session = Depends(get_db)) -> Dish:
    return await service.get(db, dish_id)


@routers.post(
    '/',
    status_code=201,
    summary='Создаем блюдо',
    tags=['dishes'],
    response_model=Dish
)
async def create(
        submenu_id: UUID,
        menu_id: UUID,
        data: DishCreate,
        db: Session = Depends(get_db)
) -> Dish:
    return await service.create(db, data, submenu_id, menu_id)


@routers.patch(
    '/{dish_id}/',
    summary='Обновляем блюдо',
    tags=['dishes'],
    response_model=DishCreate
)
async def update(
        dish_id: UUID,
        data: DishCreate,
        db: Session = Depends(get_db)
) -> Dish:
    return await service.update(db, data, dish_id)


@routers.delete(
    '/{dish_id}/',
    summary='Удаляем блюдо',
    tags=['dishes'],
)
async def delete(
        dish_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await service.delete(db, dish_id)
