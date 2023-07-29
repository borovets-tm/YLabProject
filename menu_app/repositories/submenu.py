from uuid import uuid4, UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from menu_app.models import Submenu
from menu_app.schemas.submenu import SubmenuCreate


fields: tuple = ('id', 'title', 'description', 'dishes_count')


async def get_submenus(db: Session):
    result = (
        db
        .query(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            func.count(Submenu.dishes).label('dishes_count')
        )
        .join(Submenu.dishes, isouter=True)
        .group_by(Submenu.id)
        .all()
    )
    result = [dict(zip(fields, data)) for data in result]
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
    result = (
        db
        .query(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            func.count(Submenu.dishes).label('dishes_count')
        )
        .join(Submenu.dishes, isouter=True)
        .filter(Submenu.id == submenu_id)
        .group_by(Submenu.id)
        .first()
    )
    if not result:
        return None
    result = dict(zip(fields, result))
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
