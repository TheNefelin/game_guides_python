from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def get_by_adventure(db: AsyncSession, adventure_id: int) -> list[models.AdventureImage]:
  result = await db.execute(
    select(models.AdventureImage)
    .where(models.AdventureImage.adventure_id == adventure_id)
    .order_by(models.AdventureImage.sort_order, models.AdventureImage.id)
  )
  return list(result.scalars().all())


async def get_by_id(db: AsyncSession, id: int) -> models.AdventureImage | None:
  result = await db.execute(select(models.AdventureImage).where(models.AdventureImage.id == id))
  return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> models.AdventureImage:
  item = models.AdventureImage(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.AdventureImage) -> None:
  await db.delete(item)
  await db.commit()
