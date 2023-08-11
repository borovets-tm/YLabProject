"""Модуль для инициализации роутера, не связанного с моделями приложения.\
Работает с сервисным слоем и слоем репозитория приложения."""
from fastapi import APIRouter, Depends
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
    name='full_menu'
)
async def get_tree_menu(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    Функция работает с get-запросом получения данных из БД в виде дерева.

    :param db: Экземпляр сеанса базы данных.
    :return: Список меню со связанными подменю и блюдами в виде дерева.
    """
    return await service.get_full_menu(db)
