from sqlalchemy import select, exists, func
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# COUNT ----------------------------------------------------------
async def count(db: AsyncSession, search: str | None = None) -> int:
  stmt = select(func.count(models.Game.id))
  if search:
    stmt = stmt.where(models.Game.name.ilike(f"%{search}%"))
  result = await db.execute(stmt)
  return result.scalar_one()


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, search: str | None = None) -> list[models.Game]:
  offset = (page - 1) * limit
  stmt = select(models.Game)
  if search:
    stmt = stmt.where(models.Game.name.ilike(f"%{search}%"))
  result = await db.execute(
    stmt
    .options(
      selectinload(models.Game.platforms),
      selectinload(models.Game.genres),
    )
    .order_by(models.Game.sort_order, models.Game.name)
    .offset(offset)
    .limit(limit)
  )
  return list(result.unique().scalars().all())


# EXISTS BY NAME --------------------------------------------------
async def exists_by_name(db: AsyncSession, name: str) -> bool:
  stmt = select(exists().where(models.Game.name == name))
  result = await db.execute(stmt)
  return result.scalar_one()


# EXISTS BY SLUG --------------------------------------------------
async def exists_by_slug(db: AsyncSession, slug: str) -> bool:
  stmt = select(exists().where(models.Game.slug == slug))
  result = await db.execute(stmt)
  return result.scalar_one()


# EXISTS BY ID ----------------------------------------------------
async def exists_by_id(db: AsyncSession, id: int) -> bool:
  result = await db.execute(select(exists().where(models.Game.id == id)))
  return result.scalar_one()


# DEPENDENCIES ----------------------------------------------------
async def dependency_counts(db: AsyncSession, game_id: int) -> dict[str, int]:
  result = {}
  for model in (models.Character, models.Source, models.Screenshot, models.Map, models.Guide):
    name = model.__tablename__.replace("gg_", "")
    stmt = select(func.count(model.id)).where(model.game_id == game_id)
    result[name] = (await db.execute(stmt)).scalar_one()
  return result


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> models.Game | None:
  result = await db.execute(
    select(models.Game)
    .options(
      joinedload(models.Game.platforms),
      joinedload(models.Game.genres),
    )
    .where(models.Game.id == id)
  )
  return result.unique().scalar_one_or_none()


# GET DETAIL BY ID -------------------------------------------------
async def get_detail_by_id(db: AsyncSession, id: int) -> models.Game | None:
  result = await db.execute(
    select(models.Game)
    .options(
      joinedload(models.Game.platforms),
      joinedload(models.Game.genres),
      selectinload(models.Game.screenshots),
      selectinload(models.Game.maps),
      selectinload(models.Game.characters),
      selectinload(models.Game.sources),
      selectinload(models.Game.guides).selectinload(models.Guide.adventures).selectinload(models.Adventure.images),
    )
    .where(models.Game.id == id)
  )
  return result.unique().scalar_one_or_none()


# GET DETAIL BY SLUG -----------------------------------------------
async def get_detail_by_slug(db: AsyncSession, slug: str) -> models.Game | None:
  result = await db.execute(
    select(models.Game)
    .options(
      joinedload(models.Game.platforms),
      joinedload(models.Game.genres),
      selectinload(models.Game.screenshots),
      selectinload(models.Game.maps),
      selectinload(models.Game.characters),
      selectinload(models.Game.sources),
      selectinload(models.Game.guides).selectinload(models.Guide.adventures).selectinload(models.Adventure.images),
    )
    .where(models.Game.slug == slug)
  )
  return result.unique().scalar_one_or_none()


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dict) -> models.Game:
  platform_ids = data.pop("platform_ids", [])
  genre_ids = data.pop("genre_ids", [])

  item = models.Game(**data)
  db.add(item)
  await db.flush()

  for pid in platform_ids:
    db.add(models.GamePlatform(game_id=item.id, platform_id=pid))
  for gid in genre_ids:
    db.add(models.GameGenre(game_id=item.id, genre_id=gid))

  item_id = item.id
  await db.commit()
  result = await db.execute(
    select(models.Game)
    .options(
      joinedload(models.Game.platforms),
      joinedload(models.Game.genres),
    )
    .where(models.Game.id == item_id)
  )
  return result.unique().scalar_one()


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, item: models.Game, data: dict) -> models.Game:
  platform_ids = data.pop("platform_ids", None)
  genre_ids = data.pop("genre_ids", None)

  for key, value in data.items():
    setattr(item, key, value)

  if platform_ids is not None:
    await db.execute(models.GamePlatform.__table__.delete().where(models.GamePlatform.game_id == item.id))
    for pid in platform_ids:
      db.add(models.GamePlatform(game_id=item.id, platform_id=pid))

  if genre_ids is not None:
    await db.execute(models.GameGenre.__table__.delete().where(models.GameGenre.game_id == item.id))
    for gid in genre_ids:
      db.add(models.GameGenre(game_id=item.id, genre_id=gid))

  item_id = item.id
  await db.commit()
  result = await db.execute(
    select(models.Game)
    .options(
      joinedload(models.Game.platforms),
      joinedload(models.Game.genres),
    )
    .where(models.Game.id == item_id)
  )
  return result.unique().scalar_one()


# UPDATE COVER URL ------------------------------------------------
async def set_cover_url(db: AsyncSession, game_id: int, cover_url: str | None) -> models.Game:
  result = await db.execute(select(models.Game).where(models.Game.id == game_id))
  game = result.scalar_one()
  game.cover_url = cover_url
  await db.commit()
  await db.refresh(game)
  result = await db.execute(
    select(models.Game)
    .options(
      joinedload(models.Game.platforms),
      joinedload(models.Game.genres),
    )
    .where(models.Game.id == game_id)
  )
  return result.unique().scalar_one()


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, item: models.Game) -> None:
  await db.execute(models.GamePlatform.__table__.delete().where(models.GamePlatform.game_id == item.id))
  await db.execute(models.GameGenre.__table__.delete().where(models.GameGenre.game_id == item.id))
  await db.delete(item)
  await db.commit()
