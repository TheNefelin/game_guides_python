from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.core.security import get_current_user
from src.schemas import dtos
from . import service

require_admin = get_current_user(required_roles=["admin"])

router = APIRouter(
  prefix="/screenshots",
  tags=["screenshots"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/by-game/{game_id}",
  response_model=list[dtos.ScreenshotResponse],
  status_code=HTTP_200_OK,
  summary="Get screenshots by game",
  description="Returns all screenshots for a game, without pagination.",
)
async def get_screenshots_by_game(game_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_game(db, game_id)


@router.post(
  "/upload-image",
  response_model=dtos.ScreenshotResponse,
  status_code=HTTP_201_CREATED,
)
async def create_screenshot(
  game_id: int = Form(),
  file: UploadFile = File(...),
  alt_text: str | None = Form(default=None),
  sort_order: int = Form(default=0),
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  return await service.create(db, game_id, await file.read(), alt_text, sort_order)


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
  deleted = await service.delete(db, id)
  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Screenshot not found")
