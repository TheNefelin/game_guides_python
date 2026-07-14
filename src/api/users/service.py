from sqlalchemy.orm import Session

from src.models import models
from src.schemas import dtos
from . import repository


# GET OR CREATE USER (Auth) ---------------------------------------
def get_or_create_user(db: Session, email: str) -> dtos.UserResponse:
  entity = repository.get_by_email(db, email)

  if not entity:
    entity = repository.create(db, {"email": email})

  return dtos.UserResponse.model_validate(entity)
