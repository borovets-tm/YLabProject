from uuid import uuid4, UUID

from sqlalchemy.orm import Session

from menu_app import models, schemas


async def get_menus(db: Session):
    submenus = db.query(models.Submenu).all()
    dishes = db.query(models.Dish).all()
    result = db.query(models.Menu).all()
    for obj in result:
        submenus_id = [i.id for i in submenus if i.menu_id == obj.id]
        obj.submenus_count = len(submenus_id)
        obj.dishes_count = len(
            [i.id for i in dishes if i.submenu_id in submenus_id]
        )
    return result


async def get_menu(menu_id: UUID, db: Session):
    result = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not result:
        return None
    submenus = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id
    ).all()
    submenus_id = [i.id for i in submenus]
    dishes_count = db.query(models.Dish).filter(
        models.Dish.submenu_id.in_(submenus_id)
    ).count()
    result.submenus_count = len(submenus_id)
    result.dishes_count = dishes_count
    return result


async def create_menu(data: schemas.MenuCreate, db: Session):
    menu = models.Menu(
        id=str(uuid4()),
        title=data.title,
        description=data.description
    )
    try:
        db.add(menu)
        db.commit()
        db.refresh(menu)
    except Exception as e:
        print(e)
    return menu


async def update_menu(data: schemas.MenuCreate, db: Session, menu_id: UUID):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu.title = data.title
    menu.description = data.description
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


async def remove_menu(db: Session, menu_id: UUID):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
