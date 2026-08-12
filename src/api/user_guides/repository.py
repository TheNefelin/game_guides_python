from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, user_id: UUID, guide_id: int) -> models.UserGuide | None:
  stmt = (
    select(models.UserGuide)
    .where(models.UserGuide.user_id == user_id, models.UserGuide.guide_id == guide_id)
  )
  result = await db.execute(stmt)
  return result.scalar_one_or_none()


# EXISTS ----------------------------------------------------------
async def guide_exists(db: AsyncSession, guide_id: int) -> bool:
  stmt = select(exists().where(models.Guide.id == guide_id))
  result = await db.execute(stmt)
  return result.scalar_one()


# UPSERT (marca completada o crea) ---------------------------------
async def upsert(db: AsyncSession, user_id: UUID, guide_id: int) -> models.UserGuide:
  item = await get_by_id(db, user_id, guide_id)
  now = datetime.now(timezone.utc)
  if item:
    item.is_completed = True
    item.completed_at = now
  else:
    item = models.UserGuide(
      user_id=user_id,
      guide_id=guide_id,
      is_completed=True,
      completed_at=now,
    )
    db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# UNCHECK (desmarca completada) ------------------------------------
async def uncheck(db: AsyncSession, item: models.UserGuide) -> models.UserGuide:
  item.is_completed = False
  item.completed_at = None
  await db.commit()
  await db.refresh(item)
  return item
