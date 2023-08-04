from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.menu import MenuCreate, Menu
from menu_app.services.menu_service import service

routers = APIRouter(prefix='/menus')


@routers.get(
    '/',
    summary='Получаем список меню',
    tags=['menus'],
    response_model=List[Menu]
)
async def get_list(db: Session = Depends(get_db)) -> List[Menu]:
    return await service.get_list(db)


@routers.get(
    '/{menu_id}/',
    summary='Создаем меню',
    tags=['menus'],
    response_model=Menu
)
async def get(menu_id: UUID, db: Session = Depends(get_db)) -> Menu:
    return await service.get(db, menu_id)


@routers.post(
    '/',
    summary='Создаем новое меню',
    tags=['menus'],
    status_code=201,
    response_model=Menu
)
async def create(data: MenuCreate, db: Session = Depends(get_db)) -> Menu:
    return await service.create(db, data)


@routers.patch(
    '/{menu_id}/',
    summary='Обновляем меню',
    tags=['menus'],
    response_model=MenuCreate
)
async def update(
        menu_id: UUID,
        data: MenuCreate,
        db: Session = Depends(get_db)
) -> Menu:
    return await service.update(db, data, menu_id)


@routers.delete(
    '/{menu_id}/',
    summary='Удаляем меню',
    tags=['menus']
)
async def delete(menu_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    return await service.delete(db, menu_id)
