from sqlalchemy.orm import Session

from src.api.roles import repository
from src.schemas import dtos


# GET BY ID -------------------------------------------------------
def get_by_id(db: Session, id: int) -> dtos.RoleResponse | None:
  entity = repository.get_by_id(db, id)

  if not entity:
    return None

  return dtos.RoleResponse.model_validate(entity)
