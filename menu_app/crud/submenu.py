from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from menu_app.models import Submenu, Dish
from menu_app.schemas import SubmenuCreate


async def get_submenus(db: Session):
    result = db.query(Submenu).all()
    dishes = db.query(Dish).all()
    result = jsonable_encoder(result)
    for obj in result:
        obj['id'] = str(obj['id'])
        obj['dishes_count'] = len(
            [i for i in dishes if i.submenu_id == obj.id]
        )
    return result


async def create_submenu(menu_id: int, data: SubmenuCreate, db: Session):
    submenu = Submenu(
        title=data.title,
        description=data.description,
        menu_id=menu_id
    )
    try:
        db.add(submenu)
        db.commit()
        db.refresh(submenu)
    except Exception as e:
        print(e)
    result = jsonable_encoder(
        db.query(Submenu).filter(
            Submenu.title == submenu.title
        ).first()
    )
    result['id'] = str(result['id'])
    return result


async def get_submenu(submenu_id: int, db: Session):
    result = db.query(Submenu).filter(
        Submenu.id == submenu_id
    ).first()
    if not result:
        return None
    dishes_count = db.query(Dish).filter(
        Dish.submenu_id == submenu_id
    ).count()
    result = jsonable_encoder(result)
    result['id'] = str(result['id'])
    result['dishes_count'] = dishes_count
    return result


async def update_submenu(data: SubmenuCreate, db: Session, submenu_id: int):
    submenu = db.query(Submenu).filter(
        Submenu.id == submenu_id
    ).first()
    submenu.title = data.title
    submenu.description = data.description
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


async def remove_submenu(db: Session, submenu_id: int):
    db.query(Submenu).filter(Submenu.id == submenu_id).delete()
    db.commit()