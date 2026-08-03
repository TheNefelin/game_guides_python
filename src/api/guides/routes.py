from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/guides",
  tags=["guides"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/by-game/{game_id}",
  response_model=list[dtos.GuideResponse],
  status_code=HTTP_200_OK,
  summary="Get guides by game",
  description="Returns all guides for a game, without pagination.",
)
async def get_guides_by_game(game_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_game(db, game_id)


@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.GuideResponse],
  status_code=HTTP_200_OK,
  summary="Get all guides",
  description="Returns a paginated list of guides, optionally filtered by game_id.",
)
async def get_guides(
  params: Annotated[dtos.PaginationRequest, Depends()],
  game_id: int | None = Query(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, params.page, params.limit, game_id, params.search)


@router.get(
  "/{id}",
  response_model=dtos.GuideResponse,
  status_code=HTTP_200_OK,
  summary="Get guide by ID",
  description="Returns a guide by its ID. Raises 404 if not found.",
)
async def get_guide_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_id(db, id)


@router.post(
  "/",
  response_model=dtos.GuideResponse,
  status_code=HTTP_201_CREATED,
  summary="Create guide",
  description="Creates a new guide and returns it.",
)
async def create_guide(data: dtos.GuideRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.create(db, data)


@router.put(
  "/{id}",
  response_model=dtos.GuideResponse,
  status_code=HTTP_200_OK,
  summary="Update guide",
  description="Updates a guide by its ID. Raises 404 if not found.",
)
async def update_guide(id: int, data: dtos.GuideRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.update(db, id, data)


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete guide",
  description="Deletes a guide by its ID. Raises 404 if not found.",
)
async def delete_guide(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  await service.delete(db, id)
