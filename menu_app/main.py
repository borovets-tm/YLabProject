"""Модуль запуска приложения."""
from fastapi import APIRouter, FastAPI

from menu_app.routers import app_router, dish_router, menu_router, submenu_router
from menu_app.services.app_service import service
from menu_app.services.base_service import BaseService

app: FastAPI = FastAPI(
    title='Menu API',
    version='1.0',
    description='Post information about the restaurant menu online',
)
router: APIRouter = APIRouter(prefix='/api/v1')

submenu_router.routers.include_router(dish_router.routers)
menu_router.routers.include_router(submenu_router.routers)
app_router.routers.include_router(menu_router.routers)
router.include_router(app_router.routers)
app.include_router(router)


@app.on_event('startup')
async def test():
    await service.update_db_from_excel()


@app.on_event('shutdown')
async def shutdown() -> None:
    """
    Функция вызывает функцию удаления записей кэша запросов из Redis при\
    остановке приложения.

    :return: None.
    """
    service = BaseService()
    await service.flush_redis()
