"""Модуль запуска приложения."""
from fastapi import FastAPI, APIRouter
from .routers import (
    menu_router,
    submenu_router,
    dish_router
)
from .services.config import flush_redis

app: FastAPI = FastAPI()
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
    await flush_redis()
