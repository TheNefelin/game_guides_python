from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.core.security import get_current_user
from src.schemas import dtos
from . import service

require_admin = get_current_user(required_roles=["admin"])

router = APIRouter(
  prefix="/games",
  tags=["games"],
  dependencies=[Depends(verify_api_key)],
)


# GET ALL ---------------------------------------------------------
@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.GameResponse],
  status_code=HTTP_200_OK,
  summary="Get all games",
  description="Returns a paginated list of games with their platforms and genres.",
)
async def get_games(
  page: int = 1,
  limit: int = 20,
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, page, limit)


# GET BY ID -------------------------------------------------------
@router.get(
  "/{id}",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Get game by ID",
  description="Returns a game with its platforms and genres. Raises 404 if not found.",
)
async def get_game_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_id(db, id)


# GET DETAIL BY ID ------------------------------------------------
@router.get(
  "/{id}/detail",
  response_model=dtos.GameDetailResponse,
  status_code=HTTP_200_OK,
  summary="Get game detail by ID",
  description="Returns the full enriched detail of a game with all its relations. Raises 404 if not found.",
)
async def get_game_detail_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_detail_by_id(db, id)


# GET DETAIL BY SLUG ------------------------------------------------
@router.get(
  "/by-slug/{slug}/detail",
  response_model=dtos.GameDetailResponse,
  status_code=HTTP_200_OK,
  summary="Get game detail by slug",
  description="Returns the full enriched detail of a game matching the slug. Raises 404 if not found.",
)
async def get_game_detail_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
  return await service.get_detail_by_slug(db, slug)


# CREATE ----------------------------------------------------------
@router.post(
  "/",
  response_model=dtos.GameResponse,
  status_code=HTTP_201_CREATED,
  summary="Create game",
  description="Creates a new game with platform and genre relations.",
)
async def create_game(data: dtos.GameRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.create(db, data)


# UPDATE ----------------------------------------------------------
@router.put(
  "/{id}",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Update game",
  description="Updates a game by its ID. Replaces platform/genre relations. Raises 404 if not found.",
)
async def update_game(id: int, data: dtos.GameRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.update(db, id, data)


# UPLOAD IMAGE ----------------------------------------------------
@router.post(
  "/upload-image",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Upload game cover image",
  description="Uploads a square cover image for a game. Deletes the previous image if it exists.",
)
async def upload_game_image(
  game_id: int = Form(), 
  file: UploadFile = File(...), 
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  game = await service.upload_image(db, game_id, await file.read())
  return game


# DELETE IMAGE ----------------------------------------------------
@router.delete(
  "/{id}/image",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Delete game cover image",
  description="Deletes the cover image of a game from Cloudinary and clears the cover_url field.",
)
async def delete_game_image(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.delete_image(db, id)


# DELETE ----------------------------------------------------------
@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete game",
  description="Deletes a game by its ID. Raises 404 if not found.",
)
async def delete_game(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  await service.delete(db, id)
