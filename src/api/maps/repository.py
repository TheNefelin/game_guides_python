from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def get_by_game(db: AsyncSession, game_id: int) -> list[models.Map]:
  result = await db.execute(
    select(models.Map)
    .where(models.Map.game_id == game_id)
    .order_by(models.Map.id)
  )
  return list(result.scalars().all())


async def get_by_id(db: AsyncSession, id: int) -> models.Map | None:
  result = await db.execute(select(models.Map).where(models.Map.id == id))
  return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> models.Map:
  item = models.Map(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.Map) -> None:
  await db.delete(item)
  await db.commit()
