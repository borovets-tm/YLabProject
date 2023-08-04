from fastapi import FastAPI, APIRouter
from .routers import (
    menu_router,
    submenu_router,
    dish_router
)
from .services.config import flush_redis

app = FastAPI()
router = APIRouter(prefix='/api/v1')


submenu_router.routers.include_router(dish_router.routers)
menu_router.routers.include_router(submenu_router.routers)
router.include_router(menu_router.routers)
app.include_router(router)


@app.on_event('shutdown')
async def shutdown():
    await flush_redis()

