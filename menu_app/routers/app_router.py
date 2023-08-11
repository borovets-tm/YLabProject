"""Модуль для инициализации роутера, не связанного с моделями приложения.\
Работает с сервисным слоем и слоем репозитория приложения."""
from fastapi import APIRouter, Depends
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.database import get_db
from menu_app.services.app_service import service

routers = APIRouter(prefix='')


@routers.get(
    '/',
    summary='Получаем полную версию меню',
    description=(
            'Результатом станет получения списка меню с указанием всех подменю'
            ' и блюд.'
    ),
    tags=['app'],
    name='full_menu',
    response_model=None,
)
async def get_tree_menu(db: AsyncSession = Depends(get_db)) -> Sequence:
    """
    Функция работает с get-запросом получения данных из БД в виде дерева.

    :param db: Экземпляр сеанса базы данных.
    :return: Список меню со связанными подменю и блюдами в виде дерева.
    """
    return await service.get_full_menu(db)


@routers.post(
    '/',
    summary='Обновляем базу данных меню из файла Menu.xlsx',
    description=(
        'Фоновая задача, которая сохраняет данные из файла Menu.xlsx в базу '
        'данных каждые 15 секунд.'
    ),
    tags=['app'],
    name='update_db',
    responses={
        200: {'message': 'Data updated'}
    }
)
async def update_db_from_excel(
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    """
    Функция работает с post запросом в результате которого, обновляются данные\
     из файла Menu.xlsx в БД. Функция выполняется в фоне с помощью Celery.

    :param db: Экземпляр сеанса базы данных.
    :return: Ответ об успехе.
    """
    await service.preparing_data_for_updating(db)
    return JSONResponse(
        status_code=200,
        content={
            'message': 'Data updated'
        }
    )
