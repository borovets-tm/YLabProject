"""Модуль с роутерами для модели Menu."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.menu import Menu, MenuCreate
from menu_app.services.menu_service import service

routers = APIRouter(prefix='/menus')


@routers.get(
    '/',
    summary='Получаем список меню',
    tags=['menus'],
    response_model=list[Menu]
)
async def get_list(db: Session = Depends(get_db)) -> list[Menu]:
    """
    Функция получает из слоя service информацию о списке меню и передает ее в\
    качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :return: Список меню.
    """
    return await service.get_list(db)


@routers.get(
    '/{menu_id}/',
    summary='Создаем меню',
    tags=['menus'],
    response_model=Menu
)
async def get(menu_id: UUID, db: Session = Depends(get_db)) -> Menu:
    """
    Функция получает из слоя service информацию о конкретном меню и передает\
    ее качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :param menu_id: Идентификатор меню.
    :return: Информация о меню с указанным идентификатором.
    """
    return await service.get(db, menu_id)


@routers.post(
    '/',
    summary='Создаем новое меню',
    tags=['menus'],
    status_code=201,
    response_model=Menu
)
async def create(data: MenuCreate, db: Session = Depends(get_db)) -> Menu:
    """
    Функция создает новое меню в базе данных с предоставленными данными.

    :param data: Данные для создания меню.
    :param db: Экземпляром сеанса базы данных.
    :return: Информация о созданном меню.
    """
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
    """
    Функция обновляет информацию о созданном меню, передавая информацию через\
    слой service в слой repository, после чего возвращает ответ пользователю.

    :param menu_id: Идентификатор меню.
    :param data: Обновляемая информация.
    :param db: Экземпляром сеанса базы данных.
    :return: Обновленная информация о меню.
    """
    return await service.update(db, data, menu_id)


@routers.delete(
    '/{menu_id}/',
    summary='Удаляем меню',
    tags=['menus']
)
async def delete(menu_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Функция удаляет экземпляр модели Menu.

    :param menu_id: Идентификатор меню.
    :param db: Экземпляром сеанса базы данных.
    :return: Ответ об успехе или неудачи удаления.
    """
    return await service.delete(db, menu_id)
