from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.schemas.submenu import SubmenuCreate, Submenu
from menu_app.repositories.submenu_repository import (
    repository,
    SubmenuRepository
)
from .config import set_cache, get_cache, delete_cache, flush_redis


class SubmenuService:

    def __init__(self):
        self.repository: SubmenuRepository = repository
        self.fields: tuple = (
            'id',
            'title',
            'description',
            'dishes_count'
        )

    async def get_list(self, db: Session) -> List[Submenu]:
        result = await get_cache('submenu.get_list')
        if not result:
            result = await self.repository.get_list(db)
            await set_cache('submenu.get_list', result)
        return result

    async def get(self, db: Session, submenu_id: UUID) -> Submenu:
        result = await get_cache(f'submenu.get.{submenu_id}')
        if not result:
            result = await self.repository.get(db, submenu_id)
            await set_cache(f'submenu.get.{submenu_id}', result)
        return result

    async def create(
            self,
            db: Session,
            data: SubmenuCreate,
            menu_id: UUID
    ) -> Submenu:
        await delete_cache(
            [
                'menu.get_list',
                f'menu.get{menu_id}',
                'submenu.get_list'
            ]
        )
        return await self.repository.create(db, data, menu_id)

    async def update(
            self,
            db: Session,
            data: SubmenuCreate,
            submenu_id: UUID
    ) -> Submenu:
        await delete_cache(['submenu.get_list', f'submenu.get.{submenu_id}'])
        result = await self.repository.update(db, data, submenu_id)
        return result

    async def delete(
            self,
            db: Session,
            submenu_id: UUID
    ) -> JSONResponse:
        await flush_redis()
        result = await self.repository.remove(db, submenu_id)
        return result


service = SubmenuService()
