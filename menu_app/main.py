"""Модуль запуска приложения."""
from fastapi import APIRouter, FastAPI

from .routers import dish_router, menu_router, submenu_router
from .services.base_service import BaseService

app: FastAPI = FastAPI(
    title='Menu API',
    version='1.0',
    description='Post information about the restaurant menu online',
)
router: APIRouter = APIRouter(prefix='/api/v1')

submenu_router.routers.include_router(dish_router.routers)
menu_router.routers.include_router(submenu_router.routers)
router.include_router(menu_router.routers)
app.include_router(router)


@app.on_event('shutdown')
async def shutdown() -> None:
    """
    Функция вызывает функцию удаления записей кэша запросов из Redis при\
    остановке приложения.

    :return: None.
    """
    service = BaseService()
    await service.flush_redis()
