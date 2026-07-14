from sqlalchemy.orm import Session

from src.models import models


# GET BY ID -------------------------------------------------------
def get_by_id(db: Session, id: int) -> models.Role | None:
  return (
    db.query(models.Role)
    .filter(models.Role.id == id)
    .first()
  )
