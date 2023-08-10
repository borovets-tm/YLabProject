"""Модуль с роутерами для модели Submenu."""
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.submenu import Submenu, SubmenuCreate
from menu_app.services.submenu_service import service

routers = APIRouter(prefix='/{menu_id}/submenus')


@routers.get(
    '/',
    summary='Получаем список под-меню',
    description=(
            'В ответе вернутся все экземпляры модели Подменю, находящиеся в '
            'базе данных в виде списка или пустой список, если не создавалось '
            'ни одного экземпляра.'
    ),
    tags=['submenus'],
    name='get_list_submenu',
    response_model=list[Submenu]
)
async def get_list(
        request: Request,
        db: AsyncSession = Depends(get_db)
) -> list[Submenu]:
    """
    Функция получает из слоя service информацию о списке под-меню и передает ее\
    в качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :param request: Запрос.
    :return: Список под-меню.
    """
    return await service.get_list(db, request.path_params)


@routers.get(
    '/{submenu_id}/',
    summary='Получаем под-меню',
    description='В ответе в случае успеха вернется экземпляр модели Подменю.',
    tags=['submenus'],
    name='get_submenu',
    response_model=Submenu
)
async def get(
        request: Request,
        submenu_id: UUID,
        db: AsyncSession = Depends(get_db)
) -> Submenu:
    """
    Функция получает из слоя service информацию о конкретном под-меню и\
    передает ее качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :param submenu_id: Идентификатор под-меню.
    :param request: Запрос.
    :return: Информация о под-меню с указанным идентификатором.
    """
    return await service.get(db, submenu_id, request.path_params)


@routers.post(
    '/',
    summary='Создаем под-меню',
    description=(
            'Необходимо указать название и описание под-меню, а также id '
            'существующего меню, к которому будет относиться под-меню. ID будет'
            ' сгенерирован системой. В ответе вернется информация о созданном '
            'экземпляре.'
    ),
    tags=['submenus'],
    name='create_submenu',
    status_code=201,
    response_model=Submenu
)
async def create(
        request: Request,
        menu_id: UUID,
        data: SubmenuCreate,
        db: AsyncSession = Depends(get_db)
) -> Submenu:
    """
    Функция создает новое под-меню в базе данных с предоставленными данными.

    :param request: Запрос.
    :param menu_id: Идентификатор меню, к которому относится под-меню.
    :param data: Данные для создания под-меню.
    :param db: Экземпляром сеанса базы данных.
    :return: Информация о созданном под-меню.
    """
    return await service.create(db, data, menu_id, request.path_params)


@routers.patch(
    '/{submenu_id}/',
    summary='Обновляем под-меню',
    description=(
            'Необходимо указать изменяемые данные. Ответ вернет обновленный '
            'экземпляр модели.'
    ),
    tags=['submenus'],
    name='update_submenu',
    response_model=SubmenuCreate
)
async def update(
        request: Request,
        data: SubmenuCreate,
        submenu_id: UUID,
        db: AsyncSession = Depends(get_db)
) -> Submenu:
    """
    Функция обновляет информацию о созданном под-меню, передавая информацию\
    через слой service в слой repository, после чего возвращает ответ\
    пользователю.

    :param request: Запрос.
    :param submenu_id: Идентификатор под-меню.
    :param data: Обновляемая информация.
    :param db: Экземпляром сеанса базы данных.
    :return: Обновленная информация о под-меню.
    """
    return await service.update(db, data, submenu_id, request.path_params)


@routers.delete(
    '/{submenu_id}/',
    summary='Удаляем под-меню',
    description=(
            'Результатом станет удаление экземпляра модели с указанным id. '
            'В ответе вернется информация об успехе или неудачи удаления.'
    ),
    tags=['submenus'],
    name='delete_submenu'
)
async def delete(
        request: Request,
        submenu_id: UUID,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    """
    Функция удаляет экземпляр модели Submenu.

    :param submenu_id: Идентификатор под-меню.
    :param request: Запрос.
    :param db: Экземпляром сеанса базы данных.
    :return: Ответ об успехе или неудачи удаления.
    """
    return await service.delete(db, submenu_id, request.path_params)
