from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from menu_app.models import Dish
from menu_app.schemas import DishCreate


async def get_dishes(db: Session):
    result = db.query(Dish).all()
    return result


async def create_dish(submenu_id: UUID, data: DishCreate, db: Session):
    dish = Dish(
        id=uuid4(),
        title=data.title,
        description=data.description,
        price=data.price,
        submenu_id=submenu_id
    )
    try:
        db.add(dish)
        db.commit()
        db.refresh(dish)
    except Exception as e:
        print(e)
    return dish


async def get_dish(dish_id: UUID, db: Session):
    result = db.query(Dish).filter(
        Dish.id == dish_id
    ).first()
    if not result:
        return None
    return result


async def update_dish(data: DishCreate, db: Session, dish_id: UUID):
    dish = db.query(Dish).filter(
        Dish.id == dish_id
    ).first()
    dish.title = data.title
    dish.description = data.description
    dish.price = data.price
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


async def remove_dish(db: Session, dish_id: UUID):
    db.query(Dish).filter(Dish.id == dish_id).delete()
    db.commit()
