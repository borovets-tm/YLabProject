from sqlalchemy import Column, ForeignKey, String, DECIMAL, UUID
from sqlalchemy.orm import relationship

from .database import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(
        UUID,
        primary_key=True,
        index=True
    )
    title = Column(
        String,
        unique=True,
        index=True
    )
    description = Column(
        String,
        nullable=True,
    )
    submenus = relationship('Submenu', back_populates='menu')


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(
        UUID,
        primary_key=True,
        index=True
    )
    title = Column(
        String,
        unique=True,
        index=True
    )
    description = Column(
        String,
        nullable=True
    )
    menu_id = Column(
        UUID,
        ForeignKey('menus.id', ondelete='CASCADE')
    )
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu')


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(
        UUID,
        primary_key=True,
        index=True
    )
    title = Column(
        String,
        unique=True,
        index=True
    )
    description = Column(
        String,
        nullable=True
    )
    price = Column(
        DECIMAL(precision=2)
    )
    submenu_id = Column(
        UUID,
        ForeignKey('submenus.id', ondelete='CASCADE'),
    )
    submenu = relationship('Submenu', back_populates='dishes')
