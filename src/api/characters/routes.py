from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.core.limiter import limiter
from src.core.uploads import validate_image_upload
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/characters",
  tags=["characters"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.CharacterResponse],
  status_code=HTTP_200_OK,
  summary="Get all characters",
  description="Returns a paginated list of characters, optionally filtered by game_id.",
)
async def get_characters(
  params: Annotated[dtos.PaginationRequest, Depends()],
  game_id: int | None = Query(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, params.page, params.limit, game_id, params.search)


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
@limiter.limit("10/minute")
async def upload_character_image(
  request: Request,
  id: int = Form(),
  file: UploadFile = File(...),
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  character = await service.upload_image(db, id, await validate_image_upload(file))
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
