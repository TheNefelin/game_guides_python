from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import NotFoundError
from . import repository


# CREATE (marca guía completada) -----------------------------------
async def create(db: AsyncSession, user_id: UUID, guide_id: int) -> dtos.UserGuideResponse:
  if not await repository.guide_exists(db, guide_id):
    raise NotFoundError("Guide")
  entity = await repository.upsert(db, user_id, guide_id)
  return dtos.UserGuideResponse.model_validate(entity)


# DELETE (desmarca guía) -------------------------------------------
async def delete(db: AsyncSession, user_id: UUID, guide_id: int) -> None:
  entity = await repository.get_by_id(db, user_id, guide_id)
  if not entity:
    raise NotFoundError("User guide")
  await repository.uncheck(db, entity)
