from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import NotFoundError
from . import repository


async def get_by_guide(db: AsyncSession, user_id: UUID, guide_id: int) -> list[dtos.UserAdventureResponse]:
  entities = await repository.get_by_guide(db, user_id, guide_id)
  return [dtos.UserAdventureResponse.model_validate(e) for e in entities]


async def create(db: AsyncSession, user_id: UUID, adventure_id: int) -> dtos.UserAdventureResponse:
  if not await repository.adventure_exists(db, adventure_id):
    raise NotFoundError("Adventure")
  entity = await repository.upsert(db, user_id, adventure_id)
  return dtos.UserAdventureResponse.model_validate(entity)


async def delete(db: AsyncSession, user_id: UUID, adventure_id: int) -> None:
  entity = await repository.get_by_id(db, user_id, adventure_id)
  if not entity:
    raise NotFoundError("User adventure")
  await repository.uncheck(db, entity)
