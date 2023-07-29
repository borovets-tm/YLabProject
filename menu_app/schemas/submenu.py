from pydantic import BaseModel, UUID4


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: UUID4
    dishes_count: int | None = 0
