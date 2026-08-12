from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, user_id: UUID, adventure_id: int) -> models.UserAdventure | None:
  stmt = (
    select(models.UserAdventure)
    .where(models.UserAdventure.user_id == user_id, models.UserAdventure.adventure_id == adventure_id)
  )
  result = await db.execute(stmt)
  return result.scalar_one_or_none()


# EXISTS ----------------------------------------------------------
async def adventure_exists(db: AsyncSession, adventure_id: int) -> bool:
  stmt = select(exists().where(models.Adventure.id == adventure_id))
  result = await db.execute(stmt)
  return result.scalar_one()


# UPSERT (marca completado o crea) ---------------------------------
async def upsert(db: AsyncSession, user_id: UUID, adventure_id: int) -> models.UserAdventure:
  item = await get_by_id(db, user_id, adventure_id)
  now = datetime.now(timezone.utc)
  if item:
    item.is_completed = True
    item.completed_at = now
  else:
    item = models.UserAdventure(
      user_id=user_id,
      adventure_id=adventure_id,
      is_completed=True,
      completed_at=now,
    )
    db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# UNCHECK (desmarca completado) ------------------------------------
async def uncheck(db: AsyncSession, item: models.UserAdventure) -> models.UserAdventure:
  item.is_completed = False
  item.completed_at = None
  await db.commit()
  await db.refresh(item)
  return item
