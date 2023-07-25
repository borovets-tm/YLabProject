from decimal import Decimal

from pydantic import BaseModel, UUID4


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: UUID4
    submenus_count: int | None = 0
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: UUID4
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID4

    class Config:
        orm_mode = True
