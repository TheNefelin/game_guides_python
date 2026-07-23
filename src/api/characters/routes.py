from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.dependencies import verify_api_key
from src.core.database import get_db
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
  character = await service.get_by_id(db, id)
  if not character:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Character not found")
  return character


@router.post(
  "/",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_201_CREATED,
  summary="Create character",
  description="Creates a new character and returns it.",
)
async def create_character(data: dtos.CharacterRequest, db: AsyncSession = Depends(get_db)):
  return await service.create(db, data)


@router.put(
  "/{id}",
  response_model=dtos.CharacterResponse,
  status_code=HTTP_200_OK,
  summary="Update character",
  description="Updates a character by its ID. Raises 404 if not found.",
)
async def update_character(id: int, data: dtos.CharacterRequest, db: AsyncSession = Depends(get_db)):
  character = await service.update(db, id, data)
  if not character:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Character not found")
  return character


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete character",
  description="Deletes a character by its ID. Raises 404 if not found.",
)
async def delete_character(id: int, db: AsyncSession = Depends(get_db)):
  deleted = await service.delete(db, id)
  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Character not found")
