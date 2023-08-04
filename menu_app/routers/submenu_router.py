from typing import List
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.submenu import SubmenuCreate, Submenu
from menu_app.services.submenu_service import service

routers = APIRouter(prefix='/{menu_id}/submenus')


@routers.get(
    "/",
    summary='Получаем список подменю',
    tags=['submenus'],
    response_model=list[Submenu]
)
async def get_list(db: Session = Depends(get_db)) -> List[Submenu]:
    return await service.get_list(db)


@routers.get(
    '/{submenu_id}/',
    summary='Получаем подменю',
    tags=['submenus'],
    response_model=Submenu
)
async def get(submenu_id: UUID, db: Session = Depends(get_db)) -> Submenu:
    return await service.get(db, submenu_id)


@routers.post(
    '/',
    summary='Создаем подменю',
    tags=['submenus'],
    status_code=201,
    response_model=Submenu
)
async def create(
        menu_id: UUID,
        data: SubmenuCreate,
        db: Session = Depends(get_db)
) -> Submenu:
    return await service.create(db, data, menu_id)


@routers.patch(
    '/{submenu_id}/',
    summary='Обновляем подменю',
    tags=['submenus'],
    response_model=SubmenuCreate
)
async def update(
        data: SubmenuCreate,
        submenu_id: UUID,
        db: Session = Depends(get_db)
) -> Submenu:
    return await service.update(db, data, submenu_id)


@routers.delete(
    '/{submenu_id}/',
    summary='Удаляем подменю',
    tags=['submenus']
)
async def delete(
        submenu_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await service.delete(db, submenu_id)
