from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from src.models import models


# COUNT ----------------------------------------------------------
def count(db: Session) -> int:
  return db.query(models.Platforms).count()


# GET ALL --------------------------------------------------------
def get_all(db: Session, page: int = 1, limit: int = 20) -> list[models.Platforms]:
  offset = (page - 1) * limit
  return (
    db.query(models.Platforms)
    .order_by(models.Platforms.name)
    .offset(offset)
    .limit(limit)
    .all()
  )


# EXISTS BY NAME --------------------------------------------------
def exists_by_name(db: Session, name: str) -> bool:
  stmt = select(exists().where(models.Platforms.name == name))
  return db.scalar(stmt)


# GET BY ID -------------------------------------------------------
def get_by_id(db: Session, id: int) -> models.Platforms | None:
  return (
    db.query(models.Platforms)
    .filter(models.Platforms.id == id)
    .first()
  )


# CREATE ----------------------------------------------------------
def create(db: Session, data: dict) -> models.Platforms:
  item = models.Platforms(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  return item


# UPDATE ----------------------------------------------------------
def update(db: Session, item: models.Platforms, data: dict) -> models.Platforms:
  for key, value in data.items():
    setattr(item, key, value)
  db.commit()
  db.refresh(item)
  return item


# DELETE ----------------------------------------------------------
def delete(db: Session, item: models.Platforms) -> None:
  db.delete(item)
  db.commit()
