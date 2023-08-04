"""Модуль со списком схем данных модели Dish."""
from decimal import Decimal

from pydantic import UUID4, BaseModel, Field


class DishBase(BaseModel):
    """Базовая модель данных для модели Dish."""

    title: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)


class DishCreate(DishBase):
    """Модель данных создания блюда и обновления информации о нем."""

    pass


class Dish(DishBase):
    """Модель данных для вывода информации о блюде в ответе пользователю."""

    id: UUID4
