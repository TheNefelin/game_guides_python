from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.core.limiter import limiter
from src.core.uploads import validate_image_upload
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/screenshots",
  tags=["screenshots"],
  dependencies=[Depends(verify_api_key)],
)


@router.post(
  "/upload-image",
  response_model=dtos.ScreenshotResponse,
  status_code=HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def create_screenshot(
  request: Request,
  game_id: int = Form(),
  file: UploadFile = File(...),
  alt_text: str | None = Form(default=None),
  sort_order: int = Form(default=0),
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  return await service.create(db, game_id, await validate_image_upload(file), alt_text, sort_order)


@router.delete(
  "/{id}/image",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete screenshot image",
  description="Deletes a screenshot image from Cloudinary and removes the record. Raises 404 if not found.",
)
async def delete_screenshot_image(
  id: int,
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  await service.delete(db, id)
