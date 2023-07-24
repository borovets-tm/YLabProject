from fastapi import Depends, FastAPI, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from . import models, schemas
from .database import SessionLocal, engine
from .crud import (
    menu as crud_menu,
    submenu as crud_submenu,
    dish as crud_dish
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter(prefix='/api/v1')
menu_routers = APIRouter(prefix='/menus')
submenu_routers = APIRouter(prefix='/{menu_id}/submenus')
dish_routers = APIRouter(prefix='/{submenu_id}/dishes')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@menu_routers.get("/", tags=['menus'], response_model=list[schemas.Menu])
async def get_menus(db: Session = Depends(get_db)) -> JSONResponse:
    return await crud_menu.get_menus(db)


@menu_routers.post(
    '/',
    tags=['menus'],
    status_code=201,
    response_model=schemas.Menu
)
async def create_menu(
        data: schemas.MenuCreate = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_menu.create_menu(data=data, db=db)


@menu_routers.get('/{menu_id}/', tags=['menus'], response_model=schemas.Menu)
async def get_menu(
        menu_id: int = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    menu = await crud_menu.get_menu(menu_id=menu_id, db=db)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@menu_routers.patch(
    '/{menu_id}/',
    tags=['menus'],
    response_model=schemas.MenuCreate
)
async def update_menu(
        menu_id: int = None,
        data: schemas.MenuCreate = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_menu.update_menu(data=data, menu_id=menu_id, db=db)


@menu_routers.delete('/{menu_id}/', tags=['menus'])
async def delete_menu(
        menu_id: int = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    await crud_menu.remove_menu(menu_id=menu_id, db=db)
    return JSONResponse(
        {
            "status": True,
            "message": "The menu has been deleted"
        }
    )


@submenu_routers.get(
    "/",
    tags=['submenus'],
    response_model=list[schemas.Submenu]
)
async def get_submenus(db: Session = Depends(get_db)) -> JSONResponse:
    return await crud_submenu.get_submenus(db)


@submenu_routers.post(
    '/',
    tags=['submenus'],
    status_code=201,
    response_model=schemas.Submenu
)
async def create_submenu(
        menu_id: int = None,
        data: schemas.SubmenuCreate = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_submenu.create_submenu(menu_id=menu_id, data=data, db=db)


@submenu_routers.get(
    '/{submenu_id}/',
    tags=['submenus'],
    response_model=schemas.Submenu
)
async def get_submenu(
        submenu_id: int = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    submenu = await crud_submenu.get_submenu(submenu_id=submenu_id, db=db)
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@submenu_routers.patch(
    '/{submenu_id}/',
    tags=['submenus'],
    response_model=schemas.SubmenuCreate
)
async def update_submenu(
        submenu_id: int = None,
        data: schemas.SubmenuCreate = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_submenu.update_submenu(
        data=data,
        submenu_id=submenu_id,
        db=db
    )


@submenu_routers.delete('/{submenu_id}/', tags=['submenus'])
async def delete_submenu(
        submenu_id: int = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    await crud_submenu.remove_submenu(submenu_id=submenu_id, db=db)
    return JSONResponse(
        {
            "status": True,
            "message": "The submenu has been deleted"
        }
    )


@dish_routers.get("/", tags=['dishes'], response_model=list[schemas.Dish])
async def get_dishes(db: Session = Depends(get_db)) -> JSONResponse:
    return await crud_dish.get_dishes(db)


@dish_routers.post(
    '/',
    tags=['dishes'],
    status_code=201,
    response_model=schemas.Dish
)
async def create_dish(
        submenu_id: int = None,
        data: schemas.DishCreate = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_dish.create_dish(submenu_id=submenu_id, data=data, db=db)


@dish_routers.get('/{dish_id}/', tags=['dishes'], response_model=schemas.Dish)
async def get_dish(
        dish_id: int = None,
        db: Session = Depends(get_db),
) -> JSONResponse:
    dish = await crud_dish.get_dish(dish_id=dish_id, db=db)
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@dish_routers.patch(
    '/{dish_id}/',
    tags=['dishes'],
    response_model=schemas.DishCreate
)
async def update_dish(
        dish_id: int = None,
        data: schemas.DishCreate = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_dish.update_dish(data=data, dish_id=dish_id, db=db)


@dish_routers.delete('/{dish_id}/', tags=['dishes'])
async def delete_dish(
        dish_id: int = None,
        db: Session = Depends(get_db)
) -> JSONResponse:
    await crud_dish.remove_dish(dish_id=dish_id, db=db)
    return JSONResponse(
        {
            "status": True,
            "message": "The dish has been deleted"
        }
    )


submenu_routers.include_router(dish_routers)
menu_routers.include_router(submenu_routers)
router.include_router(menu_routers)
app.include_router(router)
