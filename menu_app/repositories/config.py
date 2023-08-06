"""Модуль Конфигурация используется для вынесения общих и часто используемых\
функций."""
from uuid import UUID

from sqlalchemy.orm import Session

from menu_app.models import Dish, Menu, Submenu


class BaseRepository:
    """Базовый класс операций с репозиторием."""

    @classmethod
    async def data_commit(cls, db: Session, entity_model) -> None:
        """
        Метод сохраняет изменения в базе данных.

        :param db: Экземпляром сеанса базы данных.
        :param entity_model: Любая из моделей приложения.
        :return: None.
        """
        db.add(entity_model)
        db.commit()
        db.refresh(entity_model)

    @classmethod
    async def get_entity(
            cls,
            db: Session,
            entity_model,
            entity_id: UUID
    ) -> Menu | Submenu | Dish:
        """
        Метод для получения сущности модели по id для последующего обновления.

        :param db: Экземпляром сеанса базы данных.
        :param entity_model: Любая из моделей приложения.
        :param entity_id: ID сущности модели приложения.
        :return: Сущность любой из существующей модели.
        """
        return (
            db
            .query(entity_model)
            .filter(entity_model.id == entity_id)
            .first()
        )

    @classmethod
    async def remove_entity(
            cls,
            db: Session,
            entity_model, entity_id: UUID
    ) -> None:
        """
        Метод удаляет из базы данных сущность по указанному идентификатору.

        :param db: Экземпляром сеанса базы данных.
        :param entity_model: Любая из моделей приложения.
        :param entity_id: ID сущности модели приложения.
        :return: None.
        """
        db.query(entity_model).filter(entity_model.id == entity_id).delete()
        db.commit()
