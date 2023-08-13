"""Модуль запуска приложения."""
from fastapi import APIRouter, FastAPI

from menu_app.database import Base, async_engine
from menu_app.routers import app_router, dish_router, menu_router, submenu_router
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
async def startup() -> None:
    """
    Функция выполняет задачи при запуске системы. На текущий момент подключена\
    задача на создание моделей базы данных при запуске приложения.

    :return: None.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('shutdown')
async def shutdown() -> None:
    """
    Функция вызывает функцию удаления записей кэша запросов из Redis при\
    остановке приложения.

    :return: None.
    """
    service = BaseService()
    await service.flush_redis()
