from decimal import Decimal

from pydantic import BaseModel, UUID4


class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID4
