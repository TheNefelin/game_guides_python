from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def get_by_game(db: AsyncSession, game_id: int) -> list[models.Screenshot]:
  result = await db.execute(
    select(models.Screenshot)
    .where(models.Screenshot.game_id == game_id)
    .order_by(models.Screenshot.sort_order, models.Screenshot.id)
  )
  return list(result.scalars().all())


async def get_by_id(db: AsyncSession, id: int) -> models.Screenshot | None:
  result = await db.execute(select(models.Screenshot).where(models.Screenshot.id == id))
  return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> models.Screenshot:
  item = models.Screenshot(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.Screenshot) -> None:
  await db.delete(item)
  await db.commit()
