from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from menu_app.models import Dish
from menu_app.schemas import DishCreate


def get_dishes(db: Session):
    result = db.query(Dish).all()
    result = jsonable_encoder(result)
    for obj in result:
        obj['id'] = str(obj['id'])
    return result


def create_dish(submenu_id: int, data: DishCreate, db: Session):
    dish = Dish(
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
    result = jsonable_encoder(
        db.query(Dish).filter(
            Dish.title == dish.title
        ).first()
    )
    result['id'] = str(result['id'])
    return result


def get_dish(dish_id: int, db: Session):
    result = db.query(Dish).filter(
        Dish.id == dish_id
    ).first()
    if not result:
        return None
    result = jsonable_encoder(result)
    result['id'] = str(result['id'])
    return result


def update_dish(data: DishCreate, db: Session, dish_id: int):
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


def remove_dish(db: Session, dish_id: int):
    db.query(Dish).filter(Dish.id == dish_id).delete()
    db.commit()
    response = jsonable_encoder(
        {
            "status": True,
            "message": "The dish has been deleted"
        }
    )
    return response
