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
