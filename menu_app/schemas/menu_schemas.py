"""Модуль со списком схем данных модели Menu."""
from pydantic import UUID4, BaseModel


class MenuBase(BaseModel):
    """Базовая модель данных для модели Menu."""

    title: str
    description: str


class MenuCreate(MenuBase):
    """Модель данных создания меню и обновления информации о нем."""

    pass


class Menu(MenuBase):
    """Модель данных для вывода информации о меню в ответе пользователю."""

    id: UUID4
    submenus_count: int | None = 0
    dishes_count: int | None = 0
