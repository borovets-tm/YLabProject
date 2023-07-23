from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from menu_app import models, schemas


def get_menus(db: Session):
    submenus = db.query(models.Submenu).all()
    dishes = db.query(models.Dish).all()
    result = db.query(models.Menu).all()
    result = jsonable_encoder(result)
    for obj in result:
        submenus_id = [i.id for i in submenus if i.menu_id == obj.id]
        obj['submenus_count'] = len(submenus_id)
        obj['dishes_count'] = len(
            [i.id for i in dishes if i.submenu_id in submenus_id]
        )
        obj['id'] = str(obj['id'])
    return result


def get_menu(menu_id: int, db: Session):
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
    print(result.id)
    print(list(submenus_id))
    print(dishes_count)
    result = jsonable_encoder(result)
    result['id'] = str(result['id'])
    result['submenus_count'] = len(submenus_id)
    result['dishes_count'] = dishes_count
    return result


def create_menu(data: schemas.MenuCreate, db: Session):
    menu = models.Menu(title=data.title, description=data.description)
    try:
        db.add(menu)
        db.commit()
        db.refresh(menu)
    except Exception as e:
        print(e)
    result = jsonable_encoder(
        db.query(models.Menu).filter(models.Menu.title == menu.title).first()
    )
    result['id'] = str(result['id'])
    return result


def update_menu(data: schemas.MenuCreate, db: Session, menu_id: int):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu.title = data.title
    menu.description = data.description
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def remove_menu(db: Session, menu_id: int):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
    response = jsonable_encoder(
        {
            "status": True,
            "message": "The menu has been deleted"
        }
    )
    return response
