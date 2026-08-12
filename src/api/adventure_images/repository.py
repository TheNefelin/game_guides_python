from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> models.AdventureImage | None:
  result = await db.execute(select(models.AdventureImage).where(models.AdventureImage.id == id))
  return result.scalar_one_or_none()


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dict) -> models.AdventureImage:
  item = models.AdventureImage(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, item: models.AdventureImage) -> None:
  await db.delete(item)
  await db.commit()
