"""Модуль со списком схем данных модели Submenu."""
from pydantic import BaseModel, UUID4


class SubmenuBase(BaseModel):
    """Базовая модель данных для модели Submenu."""

    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    """Модель данных создания подменю и обновления информации о нем."""

    pass


class Submenu(SubmenuBase):
    """Модель данных для вывода информации о подменю в ответе пользователю."""

    id: UUID4
    dishes_count: int | None = 0
