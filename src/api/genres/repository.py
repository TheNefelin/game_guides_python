from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from src.models import models


# COUNT ----------------------------------------------------------
def count(db: Session) -> int:
  return db.query(models.Genre).count()


# GET ALL --------------------------------------------------------
def get_all(db: Session, page: int = 1, limit: int = 20) -> list[models.Genre]:
  offset = (page - 1) * limit
  return (
    db.query(models.Genre)
    .order_by(models.Genre.name)
    .offset(offset)
    .limit(limit)
    .all()
  )


# EXISTS BY NAME --------------------------------------------------
def exists_by_name(db: Session, name: str) -> bool:
  stmt = select(exists().where(models.Genre.name == name))
  return db.scalar(stmt)


# GET BY ID -------------------------------------------------------
def get_by_id(db: Session, id: int) -> models.Genre | None:
  return (
    db.query(models.Genre)
    .filter(models.Genre.id == id)
    .first()
  )


# CREATE ----------------------------------------------------------
def create(db: Session, data: dict) -> models.Genre:
  item = models.Genre(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  return item


# UPDATE ----------------------------------------------------------
def update(db: Session, item: models.Genre, data: dict) -> models.Genre:
  for key, value in data.items():
    setattr(item, key, value)
  db.commit()
  db.refresh(item)
  return item


# DELETE ----------------------------------------------------------
def delete(db: Session, item: models.Genre) -> None:
  db.delete(item)
  db.commit()
