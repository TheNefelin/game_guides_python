from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.core.security import get_current_user
from src.schemas import dtos
from . import service

require_admin = get_current_user(required_roles=["admin"])

router = APIRouter(
  prefix="/characters",
  tags=["characters"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/by-game/{game_id}",
  response_model=list[dtos.CharacterResponse],
  status_code=HTTP_200_OK,
  summary="Get characters by game",
  description="Returns all characters for a game, without pagination.",
)
async def get_characters_by_game(game_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_game(db, game_id)


@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.CharacterResponse],
  status_code=HTTP_200_OK,
  summary="Get all characters",
  description="Returns a paginated list of characters, optionally filtered by game_id.",
)
async def get_characters(
  page: int = 1,
  limit: int = 20,
  game_id: int | None = Query(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, page, limit, game_id)


@router.get(
  "/{id}",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_200_OK,
  summary="Get character by ID",
  description="Returns a character by its ID. Raises 404 if not found.",
)
async def get_character_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_id(db, id)


@router.post(
  "/",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_201_CREATED,
  summary="Create character",
  description="Creates a new character and returns it.",
)
async def create_character(data: dtos.CharacterRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.create(db, data)


@router.put(
  "/{id}",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_200_OK,
  summary="Update character",
  description="Updates a character by its ID. Raises 404 if not found.",
)
async def update_character(id: int, data: dtos.CharacterRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.update(db, id, data)


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete character",
  description="Deletes a character by its ID. Raises 404 if not found.",
)
async def delete_character(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  await service.delete(db, id)


# UPLOAD IMAGE ----------------------------------------------------
@router.post(
  "/upload-image",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_200_OK,
  summary="Upload character image",
  description="Uploads a square image for a character. Deletes the previous image if it exists.",
)
async def upload_character_image(
  game_id: int = Form(),
  file: UploadFile = File(...),
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  character = await service.upload_image(db, game_id, await file.read())
  return character


# DELETE IMAGE ----------------------------------------------------
@router.delete(
  "/{id}/image",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_200_OK,
  summary="Delete character image",
  description="Deletes the image of a character from Cloudinary and clears the image_url field.",
)
async def delete_character_image(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.delete_image(db, id)
