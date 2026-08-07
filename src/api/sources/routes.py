from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/sources",
  tags=["sources"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.SourceResponse],
  status_code=HTTP_200_OK,
  summary="Get all sources",
  description="Returns a paginated list of sources, optionally filtered by game_id.",
)
async def get_sources(
  params: Annotated[dtos.PaginationRequest, Depends()],
  game_id: int | None = Query(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, params.page, params.limit, game_id, params.search)


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
