from decimal import Decimal

from pydantic import BaseModel, UUID4, Field


class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID4
