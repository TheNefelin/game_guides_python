from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import NotFoundError
from . import repository


async def get_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> list[dtos.UserGuideResponse]:
  entities = await repository.get_by_game(db, user_id, game_id)
  return [dtos.UserGuideResponse.model_validate(e) for e in entities]


async def create(db: AsyncSession, user_id: UUID, guide_id: int) -> dtos.UserGuideResponse:
  if not await repository.guide_exists(db, guide_id):
    raise NotFoundError("Guide")
  entity = await repository.upsert(db, user_id, guide_id)
  return dtos.UserGuideResponse.model_validate(entity)


async def delete(db: AsyncSession, user_id: UUID, guide_id: int) -> bool:
  entity = await repository.get_by_id(db, user_id, guide_id)
  if not entity:
    return False
  await repository.uncheck(db, entity)
  return True
