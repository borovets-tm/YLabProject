from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import menu_app.models as model
from menu_app.schemas import dish as schemas
from menu_app.database import engine, get_db
from menu_app.repositories import dish as crud_dish

model.Base.metadata.create_all(bind=engine)
routers = APIRouter(prefix='/{submenu_id}/dishes')


@routers.get("/", tags=['dishes'], response_model=list[schemas.Dish])
async def get_dishes(db: Session = Depends(get_db)) -> JSONResponse:
    return await crud_dish.get_dishes(db)


@routers.post(
    '/',
    tags=['dishes'],
    status_code=201,
    response_model=schemas.Dish
)
async def create_dish(
        submenu_id: UUID,
        data: schemas.DishCreate,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_dish.create_dish(submenu_id=submenu_id, data=data, db=db)


@routers.get('/{dish_id}/', tags=['dishes'], response_model=schemas.Dish)
async def get_dish(
        dish_id: UUID,
        db: Session = Depends(get_db),
) -> JSONResponse:
    dish = await crud_dish.get_dish(dish_id=dish_id, db=db)
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@routers.patch(
    '/{dish_id}/',
    tags=['dishes'],
    response_model=schemas.DishCreate
)
async def update_dish(
        dish_id: UUID,
        data: schemas.DishCreate,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_dish.update_dish(data=data, dish_id=dish_id, db=db)


@routers.delete('/{dish_id}/', tags=['dishes'])
async def delete_dish(
        dish_id: UUID,
        db: Session = Depends(get_db),
) -> JSONResponse:
    await crud_dish.remove_dish(dish_id=dish_id, db=db)
    return JSONResponse(
        status_code=200,
        content={
            'message': 'The dish has been deleted'
        }
    )
