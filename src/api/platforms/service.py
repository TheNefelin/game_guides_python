from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import AppError, DuplicateNameError, NotFoundError
from . import repository


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, search: str | None = None) -> dtos.PaginationResponse[dtos.PlatformsResponse]:
  total = await repository.count(db, search)
  entities = await repository.get_all(db, page, limit, search)
  items = [dtos.PlatformsResponse.model_validate(e) for e in entities]

  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> dtos.PlatformsResponse:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("Platform")

  return dtos.PlatformsResponse.model_validate(entity)


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dtos.PlatformsRequest) -> dtos.PlatformsResponse:
  if await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.create(db, data.model_dump())
  return dtos.PlatformsResponse.model_validate(entity)


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, id: int, data: dtos.PlatformsRequest) -> dtos.PlatformsResponse:
  current_entity = await repository.get_by_id(db, id)

  if not current_entity:
    raise NotFoundError("Platform")

  if await repository.exists_by_name(db, data.name, exclude_id=id):
    raise DuplicateNameError(data.name)

  entity = await repository.update(db, current_entity, data.model_dump())
  return dtos.PlatformsResponse.model_validate(entity)


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("Platform")

  deps = await repository.dependency_counts(db, id)
  active = {k: v for k, v in deps.items() if v > 0}
  if active:
    names = ", ".join(f"{k} ({v})" for k, v in active.items())
    raise AppError(f"Cannot delete platform with id {id}: it has dependencies: {names}")

  await repository.delete(db, entity)
