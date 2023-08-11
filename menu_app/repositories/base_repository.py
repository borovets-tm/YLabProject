"""Модуль Конфигурация используется для вынесения общих и часто используемых\
функций."""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Базовый класс операций с репозиторием."""

    @classmethod
    async def data_commit(cls, db: AsyncSession, entity_model) -> None:
        """
        Метод сохраняет изменения в базе данных при создании и обновлении\
        сущностей.

        :param db: Экземпляром сеанса базы данных.
        :param entity_model: Любая из моделей приложения.
        :return: None.
        """
        try:
            db.add(entity_model)
            await db.commit()
            await db.refresh(entity_model)
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await db.rollback()
            raise RuntimeError(error) from e
        finally:
            await db.close()
