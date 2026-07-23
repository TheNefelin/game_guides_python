from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def count(db: AsyncSession, game_id: int | None = None) -> int:
  stmt = select(func.count(models.Source.id))
  if game_id is not None:
    stmt = stmt.where(models.Source.game_id == game_id)
  result = await db.execute(stmt)
  return result.scalar_one()


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None) -> list[models.Source]:
  offset = (page - 1) * limit
  stmt = select(models.Source).order_by(models.Source.sort_order, models.Source.name)
  if game_id is not None:
    stmt = stmt.where(models.Source.game_id == game_id)
  result = await db.execute(stmt.offset(offset).limit(limit))
  return list(result.scalars().all())


async def exists_by_name(db: AsyncSession, name: str, game_id: int) -> bool:
  stmt = select(exists().where(models.Source.name == name, models.Source.game_id == game_id))
  result = await db.execute(stmt)
  return result.scalar_one()


async def get_by_id(db: AsyncSession, id: int) -> models.Source | None:
  result = await db.execute(select(models.Source).where(models.Source.id == id))
  return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> models.Source:
  item = models.Source(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def update(db: AsyncSession, item: models.Source, data: dict) -> models.Source:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.Source) -> None:
  await db.delete(item)
  await db.commit()
