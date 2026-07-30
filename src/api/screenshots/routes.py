from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.schemas import dtos
from . import service

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
  db: AsyncSession = Depends(get_db),
):
  return await service.create(db, game_id, await file.read(), alt_text)


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
)
async def delete_screenshot(id: int, db: AsyncSession = Depends(get_db)):
  deleted = await service.delete(db, id)
  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Screenshot not found")
