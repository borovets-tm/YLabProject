from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: str
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
    id: str
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: str

    class Config:
        orm_mode = True
