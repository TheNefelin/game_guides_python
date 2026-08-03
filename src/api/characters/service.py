from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import DuplicateNameError, NotFoundError
from src.core.cloudinary import upload_image_1_1, delete_image as cloudinary_delete, extract_public_id
from src.api.games import service as games_service
from . import repository


async def get_by_game(db: AsyncSession, game_id: int) -> list[dtos.CharacterResponse]:
  entities = await repository.get_by_game(db, game_id)
  return [dtos.CharacterResponse.model_validate(e) for e in entities]


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, game_id: int | None = None) -> dtos.PaginationResponse[dtos.CharacterResponse]:
  total = await repository.count(db, game_id)
  entities = await repository.get_all(db, page, limit, game_id)
  items = [dtos.CharacterResponse.model_validate(e) for e in entities]
  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


async def get_by_id(db: AsyncSession, id: int) -> dtos.CharacterResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Character")
  return dtos.CharacterResponse.model_validate(entity)


async def create(db: AsyncSession, data: dtos.CharacterRequest) -> dtos.CharacterResponse:
  await games_service.ensure_game_exists(db, data.game_id)
  if await repository.exists_by_name(db, data.name, data.game_id):
    raise DuplicateNameError(data.name)
  if await repository.exists_by_slug(db, data.slug, data.game_id):
    raise DuplicateNameError(f"slug '{data.slug}' already exists in this game")
  entity = await repository.create(db, data.model_dump())
  return dtos.CharacterResponse.model_validate(entity)


async def update(db: AsyncSession, id: int, data: dtos.CharacterRequest) -> dtos.CharacterResponse:
  current = await repository.get_by_id(db, id)
  if not current:
    raise NotFoundError("Character")
  await games_service.ensure_game_exists(db, data.game_id)
  if await repository.exists_by_name(db, data.name, data.game_id, exclude_id=id):
    raise DuplicateNameError(data.name)
  if await repository.exists_by_slug(db, data.slug, data.game_id, exclude_id=id):
    raise DuplicateNameError(f"slug '{data.slug}' already exists in this game")
  entity = await repository.update(db, current, data.model_dump())
  return dtos.CharacterResponse.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Character")
  await repository.delete(db, entity)


async def upload_image(db: AsyncSession, id: int, file_bytes: bytes) -> dtos.CharacterResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Character")

  if entity.image_url:
    public_id = extract_public_id(entity.image_url)
    if public_id:
      cloudinary_delete(public_id)

  image_url, _ = upload_image_1_1(file_bytes, folder="characters")
  updated = await repository.update(db, entity, {"image_url": image_url})
  return dtos.CharacterResponse.model_validate(updated)


async def delete_image(db: AsyncSession, id: int) -> dtos.CharacterResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Character")

  if entity.image_url:
    public_id = extract_public_id(entity.image_url)
    if public_id:
      cloudinary_delete(public_id)

  updated = await repository.update(db, entity, {"image_url": None})
  return dtos.CharacterResponse.model_validate(updated)
