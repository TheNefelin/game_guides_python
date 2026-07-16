from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import DuplicateNameError
from . import repository


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20) -> dtos.PaginationResponse[dtos.GameResponse]:
  total = await repository.count(db)
  entities = await repository.get_all(db, page, limit)
  items = [_entity_to_response(e) for e in entities]

  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> dtos.GameResponse | None:
  entity = await repository.get_by_id(db, id)

  if not entity:
    return None

  return _entity_to_response(entity)


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dtos.GameRequest) -> dtos.GameResponse:
  if await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.create(db, data.model_dump())
  return _entity_to_response(entity)


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, id: int, data: dtos.GameRequest) -> dtos.GameResponse | None:
  current_entity = await repository.get_by_id(db, id)

  if not current_entity:
    return None

  if data.name != current_entity.name and await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.update(db, current_entity, data.model_dump())
  return _entity_to_response(entity)


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, id: int) -> bool:
  entity = await repository.get_by_id(db, id)

  if not entity:
    return False

  await repository.delete(db, entity)
  return True


# HELPERS ---------------------------------------------------------
def _entity_to_response(entity) -> dtos.GameResponse:
  return dtos.GameResponse(
    id=entity.id,
    name=entity.name,
    slug=entity.slug,
    description=entity.description,
    cover_url=entity.cover_url,
    release_year=entity.release_year,
    rating=entity.rating,
    is_enabled=entity.is_enabled,
    sort_order=entity.sort_order,
    created_at=entity.created_at.isoformat(),
    updated_at=entity.updated_at.isoformat(),
    platforms=[dtos.PlatformsResponse(id=p.id, name=p.name) for p in entity.platforms],
    genres=[dtos.GenreResponse(id=g.id, name=g.name) for g in entity.genres],
  )
