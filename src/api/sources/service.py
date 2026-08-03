from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import DuplicateNameError, NotFoundError
from . import repository


async def get_by_game(db: AsyncSession, game_id: int) -> list[dtos.SourceResponse]:
  entities = await repository.get_by_game(db, game_id)
  return [dtos.SourceResponse.model_validate(e) for e in entities]


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None) -> dtos.PaginationResponse[dtos.SourceResponse]:
  total = await repository.count(db, game_id)
  entities = await repository.get_all(db, page, limit, game_id)
  items = [dtos.SourceResponse.model_validate(e) for e in entities]
  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


async def get_by_id(db: AsyncSession, id: int) -> dtos.SourceResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Source")
  return dtos.SourceResponse.model_validate(entity)


async def create(db: AsyncSession, data: dtos.SourceRequest) -> dtos.SourceResponse:
  if await repository.exists_by_name(db, data.name, data.game_id):
    raise DuplicateNameError(data.name)
  entity = await repository.create(db, data.model_dump())
  return dtos.SourceResponse.model_validate(entity)


async def update(db: AsyncSession, id: int, data: dtos.SourceRequest) -> dtos.SourceResponse:
  current = await repository.get_by_id(db, id)
  if not current:
    raise NotFoundError("Source")
  if await repository.exists_by_name(db, data.name, data.game_id):
    raise DuplicateNameError(data.name)
  entity = await repository.update(db, current, data.model_dump())
  return dtos.SourceResponse.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Source")
  await repository.delete(db, entity)
