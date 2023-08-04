from uuid import UUID

from sqlalchemy.orm import Session


async def data_commit(db: Session, model) -> None:
    db.add(model)
    db.commit()
    db.refresh(model)


async def get_entity(db: Session, entity_model, entity_id: UUID):
    return db.query(entity_model).filter(entity_model.id == entity_id).first()


async def remove_entity(db: Session, entity_model, entity_id: UUID) -> None:
    db.query(entity_model).filter(entity_model.id == entity_id).delete()
    db.commit()
