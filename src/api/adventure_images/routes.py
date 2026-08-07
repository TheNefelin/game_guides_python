from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/adventure-images",
  tags=["adventure-images"],
  dependencies=[Depends(verify_api_key)],
)


@router.post(
  "/upload-image",
  response_model=dtos.AdventureImageResponse,
  status_code=HTTP_201_CREATED,
)
async def create_adventure_image(
  adventure_id: int = Form(),
  file: UploadFile = File(...),
  alt_text: str | None = Form(default=None),
  sort_order: int = Form(default=0),
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  return await service.create(db, adventure_id, await file.read(), alt_text, sort_order)


@router.delete(
  "/{id}/image",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete adventure image",
  description="Deletes an adventure image from Cloudinary and removes the record. Raises 404 if not found.",
)
async def delete_adventure_image(
  id: int,
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  await service.delete(db, id)
