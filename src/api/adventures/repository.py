from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def count(db: AsyncSession, guide_id: int | None = None, search: str | None = None) -> int:
  stmt = select(func.count(models.Adventure.id))
  if guide_id is not None:
    stmt = stmt.where(models.Adventure.guide_id == guide_id)
  if search:
    stmt = stmt.where(models.Adventure.description.ilike(f"%{search}%"))
  result = await db.execute(stmt)
  return result.scalar_one()


async def get_by_guide(db: AsyncSession, guide_id: int) -> list[models.Adventure]:
  stmt = (
    select(models.Adventure)
    .where(models.Adventure.guide_id == guide_id)
    .order_by(models.Adventure.sort_order, models.Adventure.id)
  )
  result = await db.execute(stmt)
  return list(result.scalars().all())


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, guide_id: int | None = None, search: str | None = None) -> list[models.Adventure]:
  offset = (page - 1) * limit
  stmt = select(models.Adventure).order_by(models.Adventure.sort_order, models.Adventure.id)
  if guide_id is not None:
    stmt = stmt.where(models.Adventure.guide_id == guide_id)
  if search:
    stmt = stmt.where(models.Adventure.description.ilike(f"%{search}%"))
  result = await db.execute(stmt.offset(offset).limit(limit))
  return list(result.scalars().all())


async def get_by_id(db: AsyncSession, id: int) -> models.Adventure | None:
  result = await db.execute(select(models.Adventure).where(models.Adventure.id == id))
  return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> models.Adventure:
  item = models.Adventure(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def update(db: AsyncSession, item: models.Adventure, data: dict) -> models.Adventure:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.Adventure) -> None:
  await db.delete(item)
  await db.commit()
