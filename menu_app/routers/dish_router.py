"""Модуль с роутерами для модели Dish."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.schemas.dish import Dish, DishCreate
from menu_app.services.dish_service import service

routers = APIRouter(prefix='/{submenu_id}/dishes')


@routers.get(
    '/',
    tags=['dishes'],
    name='get_list_dish',
    summary='Получаем список блюд',
    description=(
            'В ответе вернутся все экземпляры модели Блюда в виде списка, '
            'находящиеся в базе данных или пустой список, если не создавалось '
            'ни одного экземпляра.'
    ),
    response_model=list[Dish]
)
async def get_list(db: Session = Depends(get_db)) -> list[Dish]:
    """
    Функция получает из слоя service информацию о списке блюд и передает ее в\
    качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :return: Список блюд.
    """
    return await service.get_list(db)


@routers.get(
    '/{dish_id}/',
    summary='Получаем блюдо',
    description='В ответе в случае успеха вернется экземпляр модели Блюдо.',
    tags=['dishes'],
    name='get_dish',
    response_model=Dish
)
async def get(dish_id: UUID, db: Session = Depends(get_db)) -> Dish:
    """
    Функция получает из слоя service информацию о конкретном блюде и передает\
    ее качестве ответа на get-запрос.

    :param db: Экземпляром сеанса базы данных.
    :param dish_id: Идентификатор блюда.
    :return: Информация о блюде с указанным идентификатором.
    """
    return await service.get(db, dish_id)


@routers.post(
    '/',
    status_code=201,
    summary='Создаем блюдо',
    description=(
            'Необходимо указать название, описание и цену блюда, а также id '
            'существующего подменю, к которому будет относиться блюдо. ID будет '
            'сгенерирован системой. В ответе вернется информация о созданном '
            'экземпляре.'
    ),
    tags=['dishes'],
    name='create_dish',
    response_model=Dish
)
async def create(
        submenu_id: UUID,
        menu_id: UUID,
        data: DishCreate,
        db: Session = Depends(get_db)
) -> Dish:
    """
    Функция создает новое блюдо в базе данных с предоставленными данными.

    :param submenu_id: Идентификатор подменю, к которому относится блюдо.
    :param menu_id: Идентификатор меню, к которому относится блюдо.
    :param data: Данные для создания блюда.
    :param db: Экземпляром сеанса базы данных.
    :return: Информация о созданном блюде.
    """
    return await service.create(db, data, submenu_id, menu_id)


@routers.patch(
    '/{dish_id}/',
    summary='Обновляем блюдо',
    description=(
            'Необходимо указать изменяемые данные. Ответ вернет обновленный '
            'экземпляр модели.'
    ),
    tags=['dishes'],
    name='update_dish',
    response_model=DishCreate
)
async def update(
        dish_id: UUID,
        data: DishCreate,
        db: Session = Depends(get_db)
) -> Dish:
    """
    Функция обновляет информацию о созданном блюде, передавая информацию через\
    слой service в слой repository, после чего возвращает ответ пользователю.

    :param dish_id: Идентификатор блюда.
    :param data: Обновляемая информация.
    :param db: Экземпляром сеанса базы данных.
    :return: Обновленная информация о блюде.
    """
    return await service.update(db, data, dish_id)


@routers.delete(
    '/{dish_id}/',
    summary='Удаляем блюдо',
    description=(
            'Результатом станет удаление экземпляра модели с указанным id. '
            'В ответе вернется информация об успехе или неудачи удаления.'
    ),
    tags=['dishes'],
    name='delete_dish'
)
async def delete(
        dish_id: UUID,
        db: Session = Depends(get_db)
) -> JSONResponse:
    """
    Функция удаляет экземпляр модели Dish.

    :param dish_id: Идентификатор блюда.
    :param db: Экземпляром сеанса базы данных.
    :return: Ответ об успехе или неудачи удаления.
    """
    return await service.delete(db, dish_id)
