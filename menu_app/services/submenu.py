from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import menu_app.models as model
from menu_app.schemas import submenu as schemas
from menu_app.database import engine, get_db
from menu_app.repositories import submenu as crud_submenu

model.Base.metadata.create_all(bind=engine)
routers = APIRouter(prefix='/{menu_id}/submenus')


@routers.get(
    "/",
    tags=['submenus'],
    response_model=list[schemas.Submenu]
)
async def get_submenus(db: Session = Depends(get_db)) -> JSONResponse:
    return await crud_submenu.get_submenus(db)


@routers.post(
    '/',
    tags=['submenus'],
    status_code=201,
    response_model=schemas.Submenu
)
async def create_submenu(
        menu_id: UUID,
        data: schemas.SubmenuCreate,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_submenu.create_submenu(menu_id=menu_id, data=data, db=db)


@routers.get(
    '/{submenu_id}/',
    tags=['submenus'],
    response_model=schemas.Submenu
)
async def get_submenu(
        submenu_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    submenu = await crud_submenu.get_submenu(submenu_id=submenu_id, db=db)
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@routers.patch(
    '/{submenu_id}/',
    tags=['submenus'],
    response_model=schemas.SubmenuCreate
)
async def update_submenu(
        submenu_id: UUID,
        data: schemas.SubmenuCreate,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await crud_submenu.update_submenu(
        data=data,
        submenu_id=submenu_id,
        db=db
    )


@routers.delete('/{submenu_id}/', tags=['submenus'])
async def delete_submenu(
        submenu_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    await crud_submenu.remove_submenu(submenu_id=submenu_id, db=db)
    return JSONResponse(
        status_code=200,
        content={
            'message': 'The submenu has been deleted'
        }
    )
