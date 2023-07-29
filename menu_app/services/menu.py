from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import menu_app.models as model
from menu_app.schemas import menu as schemas
from menu_app.database import engine, get_db
from menu_app.repositories import menu as crud_menu

model.Base.metadata.create_all(bind=engine)
routers = APIRouter(prefix='/menus')


@routers.get("/", tags=['menus'], response_model=list[schemas.Menu])
async def get_menus(db: Session = Depends(get_db)) -> JSONResponse:
    return await crud_menu.get_menus(db)


@routers.post(
    '/',
    tags=['menus'],
    status_code=201,
    response_model=schemas.Menu
)
async def create_menu(
        data: schemas.MenuCreate,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_menu.create_menu(data=data, db=db)


@routers.get('/{menu_id}/', tags=['menus'], response_model=schemas.Menu)
async def get_menu(
        menu_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    menu = await crud_menu.get_menu(menu_id=menu_id, db=db)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@routers.patch(
    '/{menu_id}/',
    tags=['menus'],
    response_model=schemas.MenuCreate
)
async def update_menu(
        menu_id: UUID,
        data: schemas.MenuCreate,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_menu.update_menu(data=data, menu_id=menu_id, db=db)


@routers.delete('/{menu_id}/', tags=['menus'])
async def delete_menu(
        menu_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    await crud_menu.remove_menu(menu_id=menu_id, db=db)
    return JSONResponse(
        status_code=200,
        content={
            "message": "The menu has been deleted"
        }
    )
