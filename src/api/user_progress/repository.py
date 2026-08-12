from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


async def get_guides_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> list[models.UserGuide]:
  stmt = (
    select(models.UserGuide)
    .join(models.Guide, models.Guide.id == models.UserGuide.guide_id)
    .where(models.UserGuide.user_id == user_id, models.Guide.game_id == game_id)
    .order_by(models.Guide.sort_order, models.Guide.id)
  )
  result = await db.execute(stmt)
  return list(result.scalars().all())


async def get_adventures_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> list[models.UserAdventure]:
  stmt = (
    select(models.UserAdventure)
    .join(models.Adventure, models.Adventure.id == models.UserAdventure.adventure_id)
    .join(models.Guide, models.Guide.id == models.Adventure.guide_id)
    .where(models.UserAdventure.user_id == user_id, models.Guide.game_id == game_id)
    .order_by(models.Guide.sort_order, models.Guide.id, models.Adventure.sort_order, models.Adventure.id)
  )
  result = await db.execute(stmt)
  return list(result.scalars().all())


async def delete_guides_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> None:
  guide_ids = (
    select(models.Guide.id).where(models.Guide.game_id == game_id)
  )
  stmt = (
    update(models.UserGuide)
    .where(
      models.UserGuide.user_id == user_id,
      models.UserGuide.guide_id.in_(guide_ids),
    )
    .values(is_completed=False, completed_at=None, updated_at=datetime.now(timezone.utc))
  )
  await db.execute(stmt)


async def delete_adventures_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> None:
  adventure_ids = (
    select(models.Adventure.id)
    .join(models.Guide, models.Guide.id == models.Adventure.guide_id)
    .where(models.Guide.game_id == game_id)
  )
  stmt = (
    update(models.UserAdventure)
    .where(
      models.UserAdventure.user_id == user_id,
      models.UserAdventure.adventure_id.in_(adventure_ids),
    )
    .values(is_completed=False, completed_at=None, updated_at=datetime.now(timezone.utc))
  )
  await db.execute(stmt)


async def delete_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> None:
  await delete_guides_by_game(db, user_id, game_id)
  await delete_adventures_by_game(db, user_id, game_id)
  await db.commit()
