from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# COUNT ----------------------------------------------------------
async def count(db: AsyncSession, search: str | None = None) -> int:
  stmt = select(func.count(models.Genre.id))
  if search:
    stmt = stmt.where(models.Genre.name.ilike(f"%{search}%"))
  result = await db.execute(stmt)
  return result.scalar_one()


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, search: str | None = None) -> list[models.Genre]:
  offset = (page - 1) * limit
  stmt = select(models.Genre)
  if search:
    stmt = stmt.where(models.Genre.name.ilike(f"%{search}%"))
  result = await db.execute(
    stmt
    .order_by(models.Genre.name)
    .offset(offset)
    .limit(limit)
  )
  return list(result.scalars().all())


# EXISTS BY NAME --------------------------------------------------
async def exists_by_name(db: AsyncSession, name: str, exclude_id: int | None = None) -> bool:
  conditions = [models.Genre.name == name]
  if exclude_id is not None:
    conditions.append(models.Genre.id != exclude_id)
  stmt = select(exists().where(*conditions))
  result = await db.execute(stmt)
  return result.scalar_one()


# EXISTS BY ID -----------------------------------------------------
async def exists_by_id(db: AsyncSession, id: int) -> bool:
  result = await db.execute(select(exists().where(models.Genre.id == id)))
  return result.scalar_one()


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> models.Genre | None:
  result = await db.execute(select(models.Genre).where(models.Genre.id == id))
  return result.scalar_one_or_none()


# DEPENDENCIES ----------------------------------------------------
async def dependency_counts(db: AsyncSession, genre_id: int) -> dict[str, int]:
  result = {}
  for model in (models.GameGenre,):
    name = model.__tablename__.replace("gg_", "")
    stmt = select(func.count(model.game_id)).where(model.genre_id == genre_id)
    result[name] = (await db.execute(stmt)).scalar_one()
  return result


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
