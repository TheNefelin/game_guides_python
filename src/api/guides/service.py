from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import AppError, NotFoundError
from src.api.games import service as games_service
from . import repository


# VALIDATION ------------------------------------------------------
async def ensure_guide_exists(db: AsyncSession, guide_id: int) -> None:
  if not await repository.exists_by_id(db, guide_id):
    raise AppError(f"Guide with id {guide_id} does not exist")


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None, search: str | None = None) -> dtos.PaginationResponse[dtos.GuideResponse]:
  total = await repository.count(db, game_id, search)
  entities = await repository.get_all(db, page, limit, game_id, search)
  items = [dtos.GuideResponse.model_validate(e) for e in entities]
  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET DETAIL ALL -------------------------------------------------
async def get_detail_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None, search: str | None = None) -> dtos.PaginationResponse[dtos.GuideDetailResponse]:
  total = await repository.count(db, game_id, search)
  entities = await repository.get_all_with_adventures(db, page, limit, game_id, search)
  items = [dtos.GuideDetailResponse.model_validate(e) for e in entities]
  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> dtos.GuideResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Guide")
  return dtos.GuideResponse.model_validate(entity)


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dtos.GuideRequest) -> dtos.GuideResponse:
  await games_service.ensure_game_exists(db, data.game_id)
  entity = await repository.create(db, data.model_dump())
  return dtos.GuideResponse.model_validate(entity)


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, id: int, data: dtos.GuideRequest) -> dtos.GuideResponse:
  current = await repository.get_by_id(db, id)
  if not current:
    raise NotFoundError("Guide")
  await games_service.ensure_game_exists(db, data.game_id)
  entity = await repository.update(db, current, data.model_dump())
  return dtos.GuideResponse.model_validate(entity)


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Guide")

  deps = await repository.dependency_counts(db, id)
  active = {k: v for k, v in deps.items() if v > 0}
  if active:
    names = ", ".join(f"{k} ({v})" for k, v in active.items())
    raise AppError(f"Cannot delete guide with id {id}: it has dependencies: {names}")

  await repository.delete(db, entity)
