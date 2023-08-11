"""Модуль хранит в себе функции приложения, связанные с работой БД со всеми\
существующими сущностями."""
from sqlalchemy import Sequence, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.models import Dish, Menu, Submenu


async def get_tree_menu_repository(db: AsyncSession) -> Sequence:
    """
    Функция возвращает древовидное меню.

    :param db: Экземпляром сеанса базы данных.
    :return: Список всех меню, связанных под-меню и блюд в виде дерева JSON.
    """
    subquery = (
        select(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            Submenu.menu_id,
            func.array_agg(
                func.json_build_object(
                    'id', Dish.id,
                    'title', Dish.title,
                    'description', Dish.description,
                    'price', Dish.price
                )
            ).label('dishes')
        )
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .group_by(Submenu.id)
        .subquery('subquery')
    )
    query = (
        select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.array_agg(
                func.json_build_object(
                    'id', subquery.c.id,
                    'title', subquery.c.title,
                    'description', subquery.c.description,
                    'dishes', subquery.c.dishes
                )
            ).label('submenus')
        )
        .outerjoin(
            subquery, Menu.id == subquery.c.menu_id
        )
        .group_by(Menu.id)
    )
    result = await db.stream(query)
    curr = await result.mappings().all()
    return curr


async def merge_objects(
        db: AsyncSession,
        obj_list: list[Menu | Submenu | Dish]
) -> None:
    """
    Функция добавляет записи в БД, а если запись существует, обновит данные.

    :param db: Экземпляр сеанса базы данных.
    :param obj_list: Список объектов для добавления в БД.
    :return: None
    """
    for obj in obj_list:
        await db.merge(obj)
    await db.commit()
