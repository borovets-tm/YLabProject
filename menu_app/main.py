from fastapi import Depends, FastAPI, APIRouter
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


@menu_routers.get("/", tags=['menus'])
async def get_menus(db: Session = Depends(get_db)):
    menus = crud_menu.get_menus(db)
    return menus


@menu_routers.post('/', tags=['menus'], status_code=201)
async def create_menu(
    data: schemas.MenuCreate = None,
        db: Session = Depends(get_db)
):
    return crud_menu.create_menu(data=data, db=db)


@menu_routers.get('/{menu_id}/', tags=['menus'])
async def get_menu(menu_id: int = None, db: Session = Depends(get_db)):
    menu = crud_menu.get_menu(menu_id=menu_id, db=db)
    if menu:
        return menu
    return JSONResponse(status_code=404, content={'detail': 'menu not found'})


@menu_routers.patch('/{menu_id}/', tags=['menus'])
async def update_menu(
        menu_id: int = None,
        data: schemas.MenuCreate = None,
        db: Session = Depends(get_db)
):
    return crud_menu.update_menu(data=data, menu_id=menu_id, db=db)


@menu_routers.delete('/{menu_id}/', tags=['menus'])
async def delete_menu(menu_id: int = None, db: Session = Depends(get_db)):
    return crud_menu.remove_menu(menu_id=menu_id, db=db)


@submenu_routers.get("/", tags=['submenus'])
async def get_submenus(db: Session = Depends(get_db)):
    submenus = crud_submenu.get_submenus(db)
    return submenus


@submenu_routers.post('/', tags=['submenus'], status_code=201)
async def create_submenu(
    menu_id: int = None,
    data: schemas.SubmenuCreate = None,
    db: Session = Depends(get_db)
):
    return crud_submenu.create_submenu(menu_id=menu_id, data=data, db=db)


@submenu_routers.get('/{submenu_id}/', tags=['submenus'])
async def get_submenu(submenu_id: int = None, db: Session = Depends(get_db)):
    submenu = crud_submenu.get_submenu(submenu_id=submenu_id, db=db)
    if submenu:
        return submenu
    return JSONResponse(
        status_code=404,
        content={
            'detail': 'submenu not found'
        }
    )


@submenu_routers.patch('/{submenu_id}/', tags=['submenus'])
async def update_submenu(
        submenu_id: int = None,
        data: schemas.SubmenuCreate = None,
        db: Session = Depends(get_db)
):
    return crud_submenu.update_submenu(data=data, submenu_id=submenu_id, db=db)


@submenu_routers.delete('/{submenu_id}/', tags=['submenus'])
async def delete_submenu(
    submenu_id: int = None,
        db: Session = Depends(get_db)
):
    return crud_submenu.remove_submenu(submenu_id=submenu_id, db=db)


@dish_routers.get("/", tags=['dishes'])
async def get_dishes(db: Session = Depends(get_db)):
    dishes = crud_dish.get_dishes(db)
    return dishes


@dish_routers.post('/', tags=['dishes'], status_code=201)
async def create_dish(
    submenu_id: int = None,
    data: schemas.DishCreate = None,
    db: Session = Depends(get_db)
):
    return crud_dish.create_dish(submenu_id=submenu_id, data=data, db=db)


@dish_routers.get('/{dish_id}/', tags=['dishes'])
async def get_dish(dish_id: int = None, db: Session = Depends(get_db)):
    dish = crud_dish.get_dish(dish_id=dish_id, db=db)
    if dish:
        return dish
    return JSONResponse(
        status_code=404,
        content={
            'detail': 'dish not found'
        }
    )


@dish_routers.patch('/{dish_id}/', tags=['dishes'])
async def update_dish(
        dish_id: int = None,
        data: schemas.DishCreate = None,
        db: Session = Depends(get_db)
):
    return crud_dish.update_dish(data=data, dish_id=dish_id, db=db)


@dish_routers.delete('/{dish_id}/', tags=['dishes'])
async def delete_dish(
    dish_id: int = None,
    db: Session = Depends(get_db)
):
    return crud_dish.remove_dish(dish_id=dish_id, db=db)


submenu_routers.include_router(dish_routers)
menu_routers.include_router(submenu_routers)
router.include_router(menu_routers)
app.include_router(router)
