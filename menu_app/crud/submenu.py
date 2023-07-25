from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from menu_app.models import Submenu, Dish
from menu_app.schemas import SubmenuCreate


async def get_submenus(db: Session):
    result = db.query(Submenu).all()
    dishes = db.query(Dish).all()
    for obj in result:
        obj.dishes_count = len(
            [i for i in dishes if i.submenu_id == obj.id]
        )
    return result


async def create_submenu(menu_id: UUID, data: SubmenuCreate, db: Session):
    submenu = Submenu(
        id=uuid4(),
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
    return submenu


async def get_submenu(submenu_id: UUID, db: Session):
    result = db.query(Submenu).filter(
        Submenu.id == submenu_id
    ).first()
    if not result:
        return None
    dishes_count = db.query(Dish).filter(
        Dish.submenu_id == submenu_id
    ).count()
    result.dishes_count = dishes_count
    return result


async def update_submenu(data: SubmenuCreate, db: Session, submenu_id: UUID):
    submenu = db.query(Submenu).filter(
        Submenu.id == submenu_id
    ).first()
    submenu.title = data.title
    submenu.description = data.description
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


async def remove_submenu(db: Session, submenu_id: UUID):
    db.query(Submenu).filter(Submenu.id == submenu_id).delete()
    db.commit()
