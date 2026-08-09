from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from uuid import UUID

from src.models import models


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: UUID) -> models.User | None:
  result = await db.execute(
    select(models.User)
    .options(joinedload(models.User.role))
    .where(models.User.id == id)
  )
  return result.scalar_one_or_none()


# GET BY EMAIL ----------------------------------------------------
async def get_by_email(db: AsyncSession, email: str) -> models.User | None:
  result = await db.execute(
    select(models.User)
    .options(joinedload(models.User.role))
    .where(models.User.email == email)
  )
  return result.scalar_one_or_none()


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dict) -> models.User:
  user = models.User(**data)
  db.add(user)
  await db.commit()
  await db.refresh(user, ["role"])
  return user
