from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import AppError, NotFoundError
from src.api.guides import service as guides_service
from . import repository


# VALIDATION ------------------------------------------------------
async def ensure_adventure_exists(db: AsyncSession, adventure_id: int) -> None:
  if not await repository.get_by_id(db, adventure_id):
    raise AppError(f"Adventure with id {adventure_id} does not exist")


async def get_by_guide(db: AsyncSession, guide_id: int) -> list[dtos.AdventureResponse]:
  entities = await repository.get_by_guide(db, guide_id)
  return [dtos.AdventureResponse.model_validate(e) for e in entities]


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, guide_id: int | None = None, search: str | None = None) -> dtos.PaginationResponse[dtos.AdventureResponse]:
  total = await repository.count(db, guide_id, search)
  entities = await repository.get_all(db, page, limit, guide_id, search)
  items = [dtos.AdventureResponse.model_validate(e) for e in entities]
  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


async def get_by_id(db: AsyncSession, id: int) -> dtos.AdventureResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Adventure")
  return dtos.AdventureResponse.model_validate(entity)


async def create(db: AsyncSession, data: dtos.AdventureRequest) -> dtos.AdventureResponse:
  await guides_service.ensure_guide_exists(db, data.guide_id)
  entity = await repository.create(db, data.model_dump())
  return dtos.AdventureResponse.model_validate(entity)


async def update(db: AsyncSession, id: int, data: dtos.AdventureRequest) -> dtos.AdventureResponse:
  current = await repository.get_by_id(db, id)
  if not current:
    raise NotFoundError("Adventure")
  await guides_service.ensure_guide_exists(db, data.guide_id)
  entity = await repository.update(db, current, data.model_dump())
  return dtos.AdventureResponse.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Adventure")
  await repository.delete(db, entity)
