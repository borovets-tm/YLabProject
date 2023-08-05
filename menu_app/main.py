"""Модуль запуска приложения."""
from fastapi import APIRouter, FastAPI
from fastapi.openapi.utils import get_openapi

from .routers import dish_router, menu_router, submenu_router
from .services.config import flush_redis

app: FastAPI = FastAPI()
router: APIRouter = APIRouter(prefix='/api/v1')


submenu_router.routers.include_router(dish_router.routers)
menu_router.routers.include_router(submenu_router.routers)
router.include_router(menu_router.routers)
app.include_router(router)

openapi_schema = get_openapi(
    title='The Menu App Info API',
    version='1.0',
    description='Post information about the restaurant menu online',
    routes=router.routes
)
app.openapi_schema = openapi_schema


@app.on_event('shutdown')
async def shutdown() -> None:
    """
    Функция вызывает функцию удаления записей кэша запросов из Redis при\
    остановке приложения.

    :return: None.
    """
    await flush_redis()
