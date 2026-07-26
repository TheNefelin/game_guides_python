from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.cloudinary import upload_image_free, delete_image as cloudinary_delete, extract_public_id
from . import repository


async def get_by_game(db: AsyncSession, game_id: int) -> list[dtos.MapResponse]:
  entities = await repository.get_by_game(db, game_id)
  return [dtos.MapResponse.model_validate(e) for e in entities]


async def create(db: AsyncSession, game_id: int, file_bytes: bytes, alt_text: str | None = None) -> dtos.MapResponse:
  image_url, _ = upload_image_free(file_bytes, folder="maps")
  entity = await repository.create(db, {"game_id": game_id, "image_url": image_url, "alt_text": alt_text})
  return dtos.MapResponse.model_validate(entity)


async def delete(db: AsyncSession, id: int) -> bool:
  entity = await repository.get_by_id(db, id)
  if not entity:
    return False
  if entity.image_url:
    public_id = extract_public_id(entity.image_url)
    if public_id:
      cloudinary_delete(public_id)
  await repository.delete(db, entity)
  return True
