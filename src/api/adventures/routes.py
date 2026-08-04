from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/adventures",
  tags=["adventures"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/by-guide/{guide_id}",
  response_model=list[dtos.AdventureResponse],
  status_code=HTTP_200_OK,
  summary="Get adventures by guide",
  description="Returns all adventures for a guide, without pagination.",
)
async def get_adventures_by_guide(guide_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_guide(db, guide_id)


@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.AdventureResponse],
  status_code=HTTP_200_OK,
  summary="Get all adventures",
  description="Returns a paginated list of adventures, optionally filtered by guide_id.",
)
async def get_adventures(
  params: Annotated[dtos.PaginationRequest, Depends()],
  guide_id: int | None = Query(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, params.page, params.limit, guide_id, params.search)


@router.get(
  "/{id}",
  response_model=dtos.AdventureResponse,
  status_code=HTTP_200_OK,
  summary="Get adventure by ID",
  description="Returns an adventure by its ID. Raises 404 if not found.",
)
async def get_adventure_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_id(db, id)


@router.post(
  "/",
  response_model=dtos.AdventureResponse,
  status_code=HTTP_201_CREATED,
  summary="Create adventure",
  description="Creates a new adventure and returns it.",
)
async def create_adventure(data: dtos.AdventureRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.create(db, data)


@router.put(
  "/{id}",
  response_model=dtos.AdventureResponse,
  status_code=HTTP_200_OK,
  summary="Update adventure",
  description="Updates an adventure by its ID. Raises 404 if not found.",
)
async def update_adventure(id: int, data: dtos.AdventureRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.update(db, id, data)


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete adventure",
  description="Deletes an adventure by its ID. Raises 404 if not found.",
)
async def delete_adventure(id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  await service.delete(db, id)
