"""Модуль с роутером для модели Menu."""
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy import RowMapping, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.menu_schemas import Menu, MenuCreate
from menu_app.services.menu_service import service

routers = APIRouter(prefix='/menus')


@routers.get(
    '/',
    summary='Получаем список меню',
    description=(
            'В ответе вернутся все экземпляры модели Меню в виде списка, '
            'находящиеся в базе данных или пустой список, если не создавалось '
            'ни одного экземпляра.'
    ),
    tags=['menus'],
    response_model=list[Menu],
    name='get_list_menu'
)
async def get_list(db: AsyncSession = Depends(get_db)) -> Sequence:
    """
    Функция получает из слоя service информацию о списке меню и передает ее в\
    качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :return: Список меню.
    """
    return await service.get_list(db)


@routers.get(
    '/{menu_id}/',
    summary='Получаем экземпляр меню по id',
    description='В ответе в случае успеха вернется экземпляр модели Меню.',
    tags=['menus'],
    name='get_menu',
    response_model=Menu,
)
async def get(
        request: Request,
        menu_id: UUID,
        db: AsyncSession = Depends(get_db)
) -> RowMapping:
    """
    Функция получает из слоя service информацию о конкретном меню и передает\
    ее качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :param menu_id: Идентификатор меню.
    :param request: Запрос.
    :return: Информация о меню с указанным идентификатором.
    """
    return await service.get(db, menu_id, request.path_params)


@routers.post(
    '/',
    summary='Создаем новое меню',
    description=(
            'Необходимо указать название и описание меню, a id будет '
            'сгенерирован системой. В ответе вернется информация о созданном '
            'экземпляре.'
    ),
    tags=['menus'],
    name='create_menu',
    status_code=201,
    response_model=Menu
)
async def create(
        data: MenuCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db)
) -> Menu:
    """
    Функция создает новое меню в базе данных с предоставленными данными.

    :param data: Данные для создания меню.
    :param background_tasks: Фоновые задачи.
    :param db: Экземпляром сеанса базы данных.
    :return: Информация о созданном меню.
    """
    return await service.create(db, data, background_tasks)


@routers.patch(
    '/{menu_id}/',
    summary='Обновляем меню',
    description=(
            'Необходимо указать изменяемые данные. Ответ вернет обновленный '
            'экземпляр модели.'
    ),
    tags=['menus'],
    name='update_menu',
    response_model=MenuCreate
)
async def update(
        request: Request,
        menu_id: UUID,
        data: MenuCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db)
) -> Menu:
    """
    Функция обновляет информацию о созданном меню, передавая информацию через\
    слой service в слой repository, после чего возвращает ответ пользователю.

    :param request: Запрос.
    :param menu_id: Идентификатор меню.
    :param data: Обновляемая информация.
    :param background_tasks: Фоновые задачи.
    :param db: Экземпляром сеанса базы данных.
    :return: Обновленная информация о меню.
    """
    return await service.update(
        db,
        data,
        menu_id,
        request.path_params,
        background_tasks
    )


@routers.delete(
    '/{menu_id}/',
    summary='Удаляем меню',
    description=(
            'Результатом станет удаление экземпляра модели с указанным id. '
            'В ответе вернется информация об успехе или неудачи удаления.'
    ),
    tags=['menus'],
    name='delete_menu'
)
async def delete(
        menu_id: UUID,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    """
    Функция удаляет экземпляр модели Menu.

    :param menu_id: Идентификатор меню.
    :param background_tasks: Фоновые задачи.
    :param db: Экземпляром сеанса базы данных.
    :return: Ответ об успехе или неудачи удаления.
    """
    return await service.delete(db, menu_id, background_tasks)
