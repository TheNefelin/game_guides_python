from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def count(db: AsyncSession, game_id: int | None = None) -> int:
  stmt = select(func.count(models.Character.id))
  if game_id is not None:
    stmt = stmt.where(models.Character.game_id == game_id)
  result = await db.execute(stmt)
  return result.scalar_one()


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None) -> list[models.Character]:
  offset = (page - 1) * limit
  stmt = select(models.Character).order_by(models.Character.sort_order, models.Character.name)
  if game_id is not None:
    stmt = stmt.where(models.Character.game_id == game_id)
  result = await db.execute(stmt.offset(offset).limit(limit))
  return list(result.scalars().all())


async def exists_by_slug(db: AsyncSession, slug: str, game_id: int, exclude_id: int | None = None) -> bool:
  conditions = [models.Character.slug == slug, models.Character.game_id == game_id]
  if exclude_id is not None:
    conditions.append(models.Character.id != exclude_id)
  stmt = select(exists().where(*conditions))
  result = await db.execute(stmt)
  return result.scalar_one()


async def exists_by_name(db: AsyncSession, name: str, game_id: int, exclude_id: int | None = None) -> bool:
  conditions = [models.Character.name == name, models.Character.game_id == game_id]
  if exclude_id is not None:
    conditions.append(models.Character.id != exclude_id)
  stmt = select(exists().where(*conditions))
  result = await db.execute(stmt)
  return result.scalar_one()


async def get_by_id(db: AsyncSession, id: int) -> models.Character | None:
  result = await db.execute(select(models.Character).where(models.Character.id == id))
  return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> models.Character:
  item = models.Character(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def update(db: AsyncSession, item: models.Character, data: dict) -> models.Character:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.Character) -> None:
  await db.delete(item)
  await db.commit()
