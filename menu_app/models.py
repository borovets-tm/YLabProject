from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from .database import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(
        Integer,
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
        Integer,
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
        Integer,
        ForeignKey('menus.id', ondelete='CASCADE')
    )
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu')


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(
        Integer,
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
        DECIMAL
    )
    submenu_id = Column(
        Integer,
        ForeignKey('submenus.id', ondelete='CASCADE'),
    )
    submenu = relationship('Submenu', back_populates='dishes')
