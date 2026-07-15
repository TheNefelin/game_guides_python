from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import DuplicateNameError
from . import repository


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20) -> dtos.PaginationResponse[dtos.PlatformsResponse]:
  total = await repository.count(db)
  entities = await repository.get_all(db, page, limit)
  items = [dtos.PlatformsResponse.model_validate(e) for e in entities]

  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> dtos.PlatformsResponse | None:
  entity = await repository.get_by_id(db, id)

  if not entity:
    return None

  return dtos.PlatformsResponse.model_validate(entity)


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dtos.PlatformsRequest) -> dtos.PlatformsResponse:
  if await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.create(db, data.model_dump())
  return dtos.PlatformsResponse.model_validate(entity)


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, id: int, data: dtos.PlatformsRequest) -> dtos.PlatformsResponse | None:
  current_entity = await repository.get_by_id(db, id)

  if not current_entity:
    return None

  if await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.update(db, current_entity, data.model_dump())
  return dtos.PlatformsResponse.model_validate(entity)


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, id: int) -> bool:
  entity = await repository.get_by_id(db, id)

  if not entity:
    return False

  await repository.delete(db, entity)
  return True
