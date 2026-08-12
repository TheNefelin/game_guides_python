from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import NotFoundError
from src.core.cloudinary import upload_image_16_9, delete_image as cloudinary_delete, extract_public_id
from src.api.adventures import service as adventures_service
from . import repository


# CREATE ----------------------------------------------------------
async def create(db: AsyncSession, adventure_id: int, file_bytes: bytes, alt_text: str | None = None, sort_order: int = 0) -> dtos.AdventureImageResponse:
  await adventures_service.ensure_adventure_exists(db, adventure_id)
  image_url, _ = upload_image_16_9(file_bytes, folder="adventures")
  entity = await repository.create(db, {"adventure_id": adventure_id, "image_url": image_url, "alt_text": alt_text, "sort_order": sort_order})
  return dtos.AdventureImageResponse.model_validate(entity)


# DELETE ----------------------------------------------------------
async def delete(db: AsyncSession, id: int) -> None:
  entity = await repository.get_by_id(db, id)
  if not entity:
    raise NotFoundError("Adventure image")
  if entity.image_url:
    public_id = extract_public_id(entity.image_url)
    if public_id:
      cloudinary_delete(public_id)
  await repository.delete(db, entity)
