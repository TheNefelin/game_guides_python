from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.core.security import get_current_user
from src.schemas import dtos
from . import service

require_admin = get_current_user(required_roles=["admin"])

router = APIRouter(
  prefix="/sources",
  tags=["sources"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/by-game/{game_id}",
  response_model=list[dtos.SourceResponse],
  status_code=HTTP_200_OK,
  summary="Get sources by game",
  description="Returns all sources for a game, without pagination.",
)
async def get_sources_by_game(game_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_game(db, game_id)


@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.SourceResponse],
  status_code=HTTP_200_OK,
  summary="Get all sources",
  description="Returns a paginated list of sources, optionally filtered by game_id.",
)
async def get_sources(
  page: int = 1,
  limit: int = 20,
  game_id: int | None = Query(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, page, limit, game_id)


@router.get(
  "/{id}",
  response_model=dtos.SourceResponse,
  status_code=HTTP_200_OK,
  summary="Get source by ID",
  description="Returns a source by its ID. Raises 404 if not found.",
)
async def get_source_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_id(db, id)


@router.post(
  "/",
  response_model=dtos.SourceResponse,
  status_code=HTTP_201_CREATED,
  summary="Create source",
  description="Creates a new source and returns it.",
)
async def create_source(data: dtos.SourceRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.create(db, data)


@router.put(
  "/{id}",
  response_model=dtos.SourceResponse,
  status_code=HTTP_200_OK,
  summary="Update source",
  description="Updates a source by its ID. Raises 404 if not found.",
)
async def update_source(id: int, data: dtos.SourceRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.update(db, id, data)


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete source",
  description="Deletes a source by its ID. Raises 404 if not found.",
)
async def delete_source(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  await service.delete(db, id)
