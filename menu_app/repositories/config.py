"""Модуль Конфигурация используется для вынесения общих и часто используемых\
функций."""
from typing import Union
from uuid import UUID

from sqlalchemy.orm import Session

from menu_app.models import Menu, Submenu, Dish


async def data_commit(db: Session, model) -> None:
    """
    Функция сохраняет изменения в базе данных.

    :param db: Экземпляром сеанса базы данных.
    :param model: Любая из моделей приложения.
    :return: None.
    """
    db.add(model)
    db.commit()
    db.refresh(model)


async def get_entity(
        db: Session,
        entity_model,
        entity_id: UUID
) -> Union[Menu, Submenu, Dish]:
    """
    Функция для получения сущности модели по id для последующего обновления.

    :param db: Экземпляром сеанса базы данных.
    :param entity_model: Любая из моделей приложения.
    :param entity_id: ID сущности модели приложения.
    :return: Сущность любой из существующей модели.
    """
    return db.query(entity_model).filter(entity_model.id == entity_id).first()


async def remove_entity(db: Session, entity_model, entity_id: UUID) -> None:
    """
    Функция удаляет из базы данных сущность по указанному идентификатору.

    :param db: Экземпляром сеанса базы данных.
    :param entity_model: Любая из моделей приложения.
    :param entity_id: ID сущности модели приложения.
    :return: None.
    """
    db.query(entity_model).filter(entity_model.id == entity_id).delete()
    db.commit()
