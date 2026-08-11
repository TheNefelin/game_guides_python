from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import AppError, NotFoundError
from src.core.cloudinary import delete_image as cloudinary_delete, extract_public_id
from src.api.guides import service as guides_service
from . import repository


# VALIDATION ------------------------------------------------------
async def ensure_adventure_exists(db: AsyncSession, adventure_id: int) -> None:
  if not await repository.get_by_id(db, adventure_id):
    raise AppError(f"Adventure with id {adventure_id} does not exist")


async def get_all(db: AsyncSession, page: int = 1, limit: int = 20, guide_id: int | None = None, search: str | None = None) -> dtos.PaginationResponse[dtos.AdventureResponse]:
  total = await repository.count(db, guide_id, search)
  entities = await repository.get_all(db, page, limit, guide_id, search)
  items = [dtos.AdventureResponse.model_validate(e) for e in entities]
  return dtos.PaginationResponse(page=page, limit=limit, total=total, items=items)


async def get_by_id(db: AsyncSession, id: int) -> dtos.AdventureResponse:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Adventure")
  return dtos.AdventureResponse.model_validate(entity)


async def create(db: AsyncSession, data: dtos.AdventureRequest) -> dtos.AdventureResponse:
  await guides_service.ensure_guide_exists(db, data.guide_id)
  entity = await repository.create(db, data.model_dump())
  return dtos.AdventureResponse.model_validate(entity)


async def update(db: AsyncSession, id: int, data: dtos.AdventureRequest) -> dtos.AdventureResponse:
  current = await repository.get_by_id(db, id)
  if not current:
    raise NotFoundError("Adventure")
  await guides_service.ensure_guide_exists(db, data.guide_id)
  entity = await repository.update(db, current, data.model_dump())
  return dtos.AdventureResponse.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id_with_images(db, id)
  if not entity:
    raise NotFoundError("Adventure")

  user_count = await repository.count_user_adventures(db, id)
  if user_count > 0:
    raise AppError(f"Cannot delete adventure with id {id}: it has user progress ({user_count})")

  image_urls = [img.image_url for img in entity.images if img.image_url]
  await repository.delete(db, entity)

  for url in image_urls:
    public_id = extract_public_id(url)
    if public_id:
      cloudinary_delete(public_id)
