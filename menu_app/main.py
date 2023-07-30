from fastapi import FastAPI, APIRouter
from .services import (
    submenu,
    menu,
    dish
)

app = FastAPI()
router = APIRouter(prefix='/api/v1')


submenu.routers.include_router(dish.routers)
menu.routers.include_router(submenu.routers)
router.include_router(menu.routers)
app.include_router(router)
