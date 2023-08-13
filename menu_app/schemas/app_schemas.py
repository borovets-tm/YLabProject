"""Модуль со списком схем для вывода древовидного меню"""
from decimal import Decimal

from pydantic import UUID4, BaseModel, Field


class DishTree(BaseModel):
    id: UUID4
    title: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)


class SubmenuTree(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes: list[DishTree]


class AppBase(BaseModel):
    """Базовая модель данных для древовидного меню."""

    id: UUID4
    title: str
    description: str
    submenus: list[SubmenuTree]
