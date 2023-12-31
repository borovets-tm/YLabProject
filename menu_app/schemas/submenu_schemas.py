"""Модуль со списком схем данных модели Submenu."""
from pydantic import UUID4, BaseModel


class SubmenuBase(BaseModel):
    """Базовая модель данных для модели Submenu."""

    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    """Модель данных создания под-меню и обновления информации о нем."""

    pass


class Submenu(SubmenuBase):
    """Модель данных для вывода информации о под-меню в ответе пользователю."""

    id: UUID4
    dishes_count: int | None = 0
