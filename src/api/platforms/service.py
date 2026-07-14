from sqlalchemy.orm import Session

from src.schemas import dtos
from src.core.exceptions import DuplicateNameError
from . import repository


# GET ALL --------------------------------------------------------
def get_all(db: Session, page: int = 1, limit: int = 20) -> dtos.PaginationResponse[dtos.PlatformsResponse]:
  total = repository.count(db)
  entities = repository.get_all(db, page, limit)
  items = [dtos.PlatformsResponse.model_validate(e) for e in entities]

  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET BY ID -------------------------------------------------------
def get_by_id(db: Session, id: int) -> dtos.PlatformsResponse | None:
  entity = repository.get_by_id(db, id)

  if not entity:
    return None

  return dtos.PlatformsResponse.model_validate(entity)


# CREATE ----------------------------------------------------------
def create(db: Session, data: dtos.PlatformsRequest) -> dtos.PlatformsResponse:
  if repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = repository.create(db, data.model_dump())
  return dtos.PlatformsResponse.model_validate(entity)


# UPDATE ----------------------------------------------------------
def update(db: Session, id: int, data: dtos.PlatformsRequest) -> dtos.PlatformsResponse | None:
  current_entity = repository.get_by_id(db, id)

  if not current_entity:
    return None

  if repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = repository.update(db, current_entity, data.model_dump())
  return dtos.PlatformsResponse.model_validate(entity)


# DELETE ----------------------------------------------------------
def delete(db: Session, id: int) -> bool:
  entity = repository.get_by_id(db, id)

  if not entity:
    return False

  repository.delete(db, entity)
  return True

