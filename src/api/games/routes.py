from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.schemas import dtos
from . import service

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
  game = await service.get_by_id(db, id)

  if not game:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Game not found")

  return game


# CREATE ----------------------------------------------------------
@router.post(
  "/",
  response_model=dtos.GameResponse,
  status_code=HTTP_201_CREATED,
  summary="Create game",
  description="Creates a new game with platform and genre relations.",
)
async def create_game(data: dtos.GameRequest, db: AsyncSession = Depends(get_db)):
  return await service.create(db, data)


# UPDATE ----------------------------------------------------------
@router.put(
  "/{id}",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Update game",
  description="Updates a game by its ID. Replaces platform/genre relations. Raises 404 if not found.",
)
async def update_game(id: int, data: dtos.GameRequest, db: AsyncSession = Depends(get_db)):
  game = await service.update(db, id, data)

  if not game:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Game not found")

  return game


# UPLOAD IMAGE ----------------------------------------------------
@router.post(
  "/{id}/upload-image",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Upload game cover image",
  description="Uploads a square cover image for a game. Deletes the previous image if it exists.",
)
async def upload_game_image(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
  game = await service.upload_image(db, id, await file.read())

  if not game:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Game not found")

  return game


# DELETE IMAGE ----------------------------------------------------
@router.delete(
  "/{id}/image",
  response_model=dtos.GameResponse,
  status_code=HTTP_200_OK,
  summary="Delete game cover image",
  description="Deletes the cover image of a game from Cloudinary and clears the cover_url field.",
)
async def delete_game_image(id: int, db: AsyncSession = Depends(get_db)):
  game = await service.delete_image(db, id)

  if not game:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Game not found")

  return game


# DELETE ----------------------------------------------------------
@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete game",
  description="Deletes a game by its ID. Raises 404 if not found.",
)
async def delete_game(id: int, db: AsyncSession = Depends(get_db)):
  deleted = await service.delete(db, id)

  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Game not found")
