"""Модуль инициализации моделей, используемых в приложении."""
import decimal
import uuid

from sqlalchemy import UUID, Column, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, relationship

from menu_app.database.postgres import Base, async_engine


class Menu(Base):
    """Класс Меню, который будет хранить в себе меню ресторана(бизнес-ланч, \
    основное, летнее и т.п.)."""

    __tablename__ = 'menus'
    id: Mapped[uuid.UUID] = Column(
        UUID,
        primary_key=True,
        index=True
    )
    title: Mapped[str] = Column(
        String,
        unique=True,
        index=True
    )
    description: Mapped[str] = Column(
        String,
        nullable=True,
    )
    submenus: Mapped[list['Submenu']] = relationship(
        'Submenu',
        back_populates='menu'
    )


class Submenu(Base):
    """Класс Подменю, который будет хранить в себе информацию о категориях\
        блюд в меню ресторана."""

    __tablename__ = 'submenus'
    id: Mapped[uuid.UUID] = Column(
        UUID,
        primary_key=True,
        index=True
    )
    title: Mapped[str] = Column(
        String,
        unique=True,
        index=True
    )
    description: Mapped[str] = Column(
        String,
        nullable=True,
    )
    menu_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey('menus.id', ondelete='CASCADE')
    )
    menu: Mapped[list['Menu']] = relationship(
        'Menu',
        back_populates='submenus'
    )
    dishes: Mapped[list['Dish']] = relationship(
        'Dish',
        back_populates='submenu'
    )


class Dish(Base):
    """Класс Блюда, который будет хранить в себе информацию о блюдах\
    ресторана."""

    __tablename__ = 'dishes'
    id: Mapped[uuid.UUID] = Column(
        UUID,
        primary_key=True,
        index=True
    )
    title: Mapped[str] = Column(
        String,
        unique=True,
        index=True
    )
    description: Mapped[str] = Column(
        String,
        nullable=True,
    )
    price: Mapped[decimal.Decimal] = Column(
        Numeric(10, 2)
    )
    submenu_id: Mapped[uuid.UUID] = Column(
        UUID,
        ForeignKey('submenus.id', ondelete='CASCADE'),
    )
    submenu: Mapped[list['Submenu']] = relationship(
        'Submenu',
        back_populates='dishes'
    )


async def init_models():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
