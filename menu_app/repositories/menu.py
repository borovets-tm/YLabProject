from uuid import uuid4, UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce

from menu_app.schemas.menu import MenuCreate
from menu_app.models import Menu
from menu_app.models import Submenu
from menu_app.models import Dish


fields: tuple = (
    'id',
    'title',
    'description',
    'submenus_count',
    'dishes_count'
)


async def get_menus(db: Session):
    # smtp = text(
    #     'SELECT menus.id AS id, '
    #     'menus.title AS title, '
    #     'menus.description AS description, '
    #     'count(submenus.menu_id) AS submenus_count, '
    #     'COALESCE(submenus.dishes_count, 0) AS dishes_count '
    #     'FROM menus '
    #     'LEFT JOIN ('
    #     'SELECT submenus.menu_id AS menu_id, '
    #     'count(dishes.id) AS dishes_count '
    #     'FROM submenus '
    #     'LEFT JOIN dishes ON submenus.id = dishes.submenu_id '
    #     'GROUP BY submenus.menu_id '
    #     ') submenus ON menus.id = submenus.menu_id '
    #     'GROUP BY menus.id, submenus.dishes_count'
    # )
    submenus = (
        db
        .query(
            Submenu.menu_id,
            func.count(Dish.id).label('dishes_count')
        )
        .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
        .group_by(Submenu.menu_id)
        .subquery('submenus')
    )
    result = (
        db
        .query(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(submenus.c.menu_id).label('submenus_count'),
            coalesce(submenus.c.dishes_count, 0).label('dishes_count')
        )
        .join(
            submenus, Menu.id == submenus.c.menu_id, isouter=True
        )
        .group_by(Menu.id, submenus.c.dishes_count)
        .all()
    )
    result = [dict(zip(fields, data)) for data in result]
    return result


async def get_menu(menu_id: UUID, db: Session):
    # smtp = text(
    #     'SELECT menus.id AS id, '
    #     'menus.title AS title, '
    #     'menus.description AS description, '
    #     'count(submenus.menu_id) AS submenus_count, '
    #     'COALESCE(submenus.dishes_count, 0) AS dishes_count '
    #     'FROM menus '
    #     'LEFT JOIN ('
    #     'SELECT submenus.menu_id AS menu_id, '
    #     'count(dishes.id) AS dishes_count '
    #     'FROM submenus '
    #     'LEFT JOIN dishes ON submenus.id = dishes.submenu_id '
    #     'GROUP BY submenus.menu_id '
    #     ') submenus ON menus.id = submenus.menu_id '
    #     'WHERE menus.id = \'%s\' '
    #     'GROUP BY menus.id, submenus.dishes_count' % menu_id
    # )
    submenus = (
        db
        .query(
            Submenu.menu_id,
            func.count(Dish.id).label('dishes_count')
        )
        .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
        .filter(Submenu.menu_id == menu_id)
        .group_by(Submenu.menu_id)
        .subquery('submenus')
    )
    result = (
        db
        .query(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(submenus.c.menu_id).label('submenus_count'),
            coalesce(submenus.c.dishes_count, 0).label('dishes_count')
        )
        .join(
            submenus, Menu.id == submenus.c.menu_id, isouter=True
        )
        .filter(Menu.id == menu_id)
        .group_by(Menu.id, submenus.c.dishes_count)
        .first()
    )
    if not result:
        return None
    result = dict(zip(fields, result))
    return result


async def create_menu(data: MenuCreate, db: Session):
    menu = Menu(
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


async def update_menu(data: MenuCreate, db: Session, menu_id: UUID):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    menu.title = data.title
    menu.description = data.description
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


async def remove_menu(db: Session, menu_id: UUID):
    db.query(Menu).filter(Menu.id == menu_id).delete()
    db.commit()
