from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# COUNT ----------------------------------------------------------
async def count(db: AsyncSession) -> int:
  result = await db.execute(select(func.count(models.Platforms.id)))
  return result.scalar_one()


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20) -> list[models.Platforms]:
  offset = (page - 1) * limit
  result = await db.execute(
    select(models.Platforms)
    .order_by(models.Platforms.name)
    .offset(offset)
    .limit(limit)
  )
  return list(result.scalars().all())


# EXISTS BY NAME --------------------------------------------------
async def exists_by_name(db: AsyncSession, name: str) -> bool:
  stmt = select(exists().where(models.Platforms.name == name))
  result = await db.execute(stmt)
  return result.scalar_one()


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> models.Platforms | None:
  result = await db.execute(select(models.Platforms).where(models.Platforms.id == id))
  return result.scalar_one_or_none()


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dict) -> models.Platforms:
  item = models.Platforms(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, item: models.Platforms, data: dict) -> models.Platforms:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, item: models.Platforms) -> None:
  await db.delete(item)
  await db.commit()
