from typing import List
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.models import Submenu
from menu_app.schemas.submenu import SubmenuCreate
from .config import data_commit, get_entity, remove_entity


class SubmenuRepository:

    def __init__(self):
        self.model = Submenu

    async def get_list(self, db: Session) -> List[Submenu]:
        query = (
            db
            .query(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(self.model.dishes).label('dishes_count')
            )
            .outerjoin(self.model.dishes)
            .group_by(self.model.id)
            .all()
        )
        return query

    async def get(self, db: Session, submenu_id: UUID) -> Submenu:
        result = (
            db
            .query(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(self.model.dishes).label('dishes_count')
            )
            .join(self.model.dishes, isouter=True)
            .filter(self.model.id == submenu_id)
            .group_by(self.model.id)
            .first()
        )
        if not result:
            raise HTTPException(status_code=404, detail='submenu not found')
        return result

    async def create(
            self,
            db: Session,
            data: SubmenuCreate,
            menu_id: UUID
    ) -> Submenu:
        submenu = self.model(
            id=uuid4(),
            title=data.title,
            description=data.description,
            menu_id=menu_id
        )
        try:
            await data_commit(db, submenu)
        except Exception as e:
            print(e)
        return submenu

    async def update(
            self,
            db: Session,
            data: SubmenuCreate,
            submenu_id: UUID
    ) -> Submenu:
        submenu = await get_entity(db, self.model, submenu_id)
        submenu.title = data.title
        submenu.description = data.description
        await data_commit(db, submenu)
        return submenu

    async def remove(self, db: Session, submenu_id: UUID) -> JSONResponse:
        try:
            await remove_entity(db, self.model, submenu_id)
            return JSONResponse(
                status_code=200,
                content={
                    'message': 'The submenu has been deleted'
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=404,
                content={
                    'message': e
                }
            )


repository = SubmenuRepository()
