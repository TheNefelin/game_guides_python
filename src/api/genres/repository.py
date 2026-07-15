from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# COUNT ----------------------------------------------------------
async def count(db: AsyncSession) -> int:
  result = await db.execute(select(func.count(models.Genre.id)))
  return result.scalar_one()


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20) -> list[models.Genre]:
  offset = (page - 1) * limit
  result = await db.execute(
    select(models.Genre)
    .order_by(models.Genre.name)
    .offset(offset)
    .limit(limit)
  )
  return list(result.scalars().all())


# EXISTS BY NAME --------------------------------------------------
async def exists_by_name(db: AsyncSession, name: str) -> bool:
  stmt = select(exists().where(models.Genre.name == name))
  result = await db.execute(stmt)
  return result.scalar_one()


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> models.Genre | None:
  result = await db.execute(select(models.Genre).where(models.Genre.id == id))
  return result.scalar_one_or_none()


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dict) -> models.Genre:
  item = models.Genre(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, item: models.Genre, data: dict) -> models.Genre:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, item: models.Genre) -> None:
  await db.delete(item)
  await db.commit()
