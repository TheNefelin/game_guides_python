from sqlalchemy import select, func, exists
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def count(db: AsyncSession, game_id: int | None = None, search: str | None = None) -> int:
  stmt = select(func.count(models.Guide.id))
  if game_id is not None:
    stmt = stmt.where(models.Guide.game_id == game_id)
  if search:
    stmt = stmt.where(models.Guide.title.ilike(f"%{search}%"))
  result = await db.execute(stmt)
  return result.scalar_one()


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None, search: str | None = None) -> list[models.Guide]:
  offset = (page - 1) * limit
  stmt = select(models.Guide).order_by(models.Guide.sort_order, models.Guide.id)
  if game_id is not None:
    stmt = stmt.where(models.Guide.game_id == game_id)
  if search:
    stmt = stmt.where(models.Guide.title.ilike(f"%{search}%"))
  result = await db.execute(stmt.offset(offset).limit(limit))
  return list(result.scalars().all())


async def get_all_with_adventures(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None, search: str | None = None) -> list[models.Guide]:
  offset = (page - 1) * limit
  stmt = select(models.Guide).options(
    selectinload(models.Guide.adventures).selectinload(models.Adventure.images)
  )
  if game_id is not None:
    stmt = stmt.where(models.Guide.game_id == game_id)
  if search:
    stmt = stmt.where(models.Guide.title.ilike(f"%{search}%"))
  result = await db.execute(stmt.order_by(models.Guide.sort_order, models.Guide.id).offset(offset).limit(limit))
  return list(result.scalars().all())


async def get_by_id(db: AsyncSession, id: int) -> models.Guide | None:
  result = await db.execute(select(models.Guide).where(models.Guide.id == id))
  return result.scalar_one_or_none()


async def exists_by_id(db: AsyncSession, id: int) -> bool:
  stmt = select(exists().where(models.Guide.id == id))
  result = await db.execute(stmt)
  return result.scalar_one()


# DEPENDENCIES ----------------------------------------------------
async def dependency_counts(db: AsyncSession, guide_id: int) -> dict[str, int]:
  result = {}
  stmt = select(func.count(models.Adventure.id)).where(models.Adventure.guide_id == guide_id)
  result["adventures"] = (await db.execute(stmt)).scalar_one()
  stmt = select(func.count(models.UserGuide.guide_id)).where(models.UserGuide.guide_id == guide_id)
  result["user_guides"] = (await db.execute(stmt)).scalar_one()
  return result


async def create(db: AsyncSession, data: dict) -> models.Guide:
  item = models.Guide(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


async def update(db: AsyncSession, item: models.Guide, data: dict) -> models.Guide:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


async def delete(db: AsyncSession, item: models.Guide) -> None:
  await db.delete(item)
  await db.commit()
