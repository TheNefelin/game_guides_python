
from sqlalchemy.orm import Session, joinedload

from src.models import models


# GET BY EMAIL ----------------------------------------------------
def get_by_email(db: Session, email: str) -> models.User | None:
  return (
    db.query(models.User)
    .options(
      joinedload(models.User.role),     
    )
    .filter(models.User.email == email)
    .first()
  )


# CREATE ----------------------------------------------------------
def create(db: Session, data: dict) -> models.User:
  user = models.User(**data)
  db.add(user)
  db.commit()
  db.refresh(user)
  return user
