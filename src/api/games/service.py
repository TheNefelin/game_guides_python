from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import DuplicateNameError, NotFoundError
from src.core.cloudinary import upload_image_1_1 as cloudinary_upload, delete_image as cloudinary_delete, extract_public_id
from . import repository


# GET ALL --------------------------------------------------------
async def get_all(db: AsyncSession, page: int = 1, limit: int = 20) -> dtos.PaginationResponse[dtos.GameResponse]:
  total = await repository.count(db)
  entities = await repository.get_all(db, page, limit)
  items = [dtos.GameResponse.model_validate(e) for e in entities]

  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> dtos.GameResponse:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("Game")

  return dtos.GameResponse.model_validate(entity)


# GET DETAIL BY ID -------------------------------------------------
async def get_detail_by_id(db: AsyncSession, id: int) -> dtos.GameDetailResponse:
  entity = await repository.get_detail_by_id(db, id)

  if not entity:
    raise NotFoundError("Game")

  return dtos.GameDetailResponse.model_validate(entity)


# GET DETAIL BY SLUG -----------------------------------------------
async def get_detail_by_slug(db: AsyncSession, slug: str) -> dtos.GameDetailResponse:
  entity = await repository.get_detail_by_slug(db, slug)

  if not entity:
    raise NotFoundError("Game")

  return dtos.GameDetailResponse.model_validate(entity)


# EXISTS BY ID -----------------------------------------------------
async def exists(db: AsyncSession, id: int) -> bool:
  return await repository.exists_by_id(db, id)


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, data: dtos.GameRequest) -> dtos.GameResponse:
  if await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.create(db, data.model_dump())
  return dtos.GameResponse.model_validate(entity)


# UPDATE ----------------------------------------------------------
async def update(db: AsyncSession, id: int, data: dtos.GameRequest) -> dtos.GameResponse:
  current_entity = await repository.get_by_id(db, id)

  if not current_entity:
    raise NotFoundError("Game")

  if data.name != current_entity.name and await repository.exists_by_name(db, data.name):
    raise DuplicateNameError(data.name)

  entity = await repository.update(db, current_entity, data.model_dump())
  return dtos.GameResponse.model_validate(entity)


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("Game")

  await repository.delete(db, entity)


# UPLOAD IMAGE ---------------------------------------------------
async def upload_image(db: AsyncSession, id: int, file_bytes: bytes) -> dtos.GameResponse:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("Game")

  if entity.cover_url:
    public_id = extract_public_id(entity.cover_url)
    if public_id:
      cloudinary_delete(public_id)

  cover_url, _ = cloudinary_upload(file_bytes, folder="games")
  entity = await repository.set_cover_url(db, id, cover_url)
  return dtos.GameResponse.model_validate(entity)


# DELETE IMAGE ----------------------------------------------------
async def delete_image(db: AsyncSession, id: int) -> dtos.GameResponse:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("Game")

  if entity.cover_url:
    public_id = extract_public_id(entity.cover_url)
    if public_id:
      cloudinary_delete(public_id)

  entity = await repository.set_cover_url(db, id, None)
  return dtos.GameResponse.model_validate(entity)
