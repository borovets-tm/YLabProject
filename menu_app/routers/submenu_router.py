"""Модуль с роутерами для модели Submenu."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.submenu import Submenu, SubmenuCreate
from menu_app.services.submenu_service import service

routers = APIRouter(prefix='/{menu_id}/submenus')


@routers.get(
    '/',
    summary='Получаем список подменю',
    tags=['submenus'],
    response_model=list[Submenu]
)
async def get_list(db: Session = Depends(get_db)) -> list[Submenu]:
    """
    Функция получает из слоя service информацию о списке подменю и передает ее\
    в качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :return: Список подменю.
    """
    return await service.get_list(db)


@routers.get(
    '/{submenu_id}/',
    summary='Получаем подменю',
    tags=['submenus'],
    response_model=Submenu
)
async def get(submenu_id: UUID, db: Session = Depends(get_db)) -> Submenu:
    """
    Функция получает из слоя service информацию о конкретном подменю и\
    передает ее качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :param submenu_id: Идентификатор подменю.
    :return: Информация о подменю с указанным идентификатором.
    """
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
    """
    Функция создает новое подменю в базе данных с предоставленными данными.

    :param menu_id: Идентификатор меню, к которому относится подменю.
    :param data: Данные для создания подменю.
    :param db: Экземпляром сеанса базы данных.
    :return: Информация о созданном подменю.
    """
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
    """
    Функция обновляет информацию о созданном подменю, передавая информацию\
    через слой service в слой repository, после чего возвращает ответ\
    пользователю.

    :param submenu_id: Идентификатор подменю.
    :param data: Обновляемая информация.
    :param db: Экземпляром сеанса базы данных.
    :return: Обновленная информация о подменю.
    """
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
    """
    Функция удаляет экземпляр модели Submenu.

    :param submenu_id: Идентификатор подменю.
    :param db: Экземпляром сеанса базы данных.
    :return: Ответ об успехе или неудачи удаления.
    """
    return await service.delete(db, submenu_id)
