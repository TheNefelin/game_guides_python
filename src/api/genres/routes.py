from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_admin
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/genres",
  tags=["genres"],
  dependencies=[Depends(verify_api_key)],
)


# GET ALL ---------------------------------------------------------
@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.GenreResponse],
  status_code=HTTP_200_OK,
  summary="Get all genres",
  description="Returns a paginated list of genres ordered by name.",
)
async def get_all_genres(
  params: Annotated[dtos.PaginationRequest, Depends()],
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, params.page, params.limit, params.search)


# GET BY ID -------------------------------------------------------
@router.get(
  "/{id}",
  response_model=dtos.GenreResponse,
  status_code=HTTP_200_OK,
  summary="Get genre by ID",
  description="Returns a genre by its ID. Raises 404 if not found.",
)
async def get_genre_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_by_id(db, id)


# CREATE ----------------------------------------------------------
@router.post(
  "/",
  response_model=dtos.GenreResponse,
  status_code=HTTP_201_CREATED,
  summary="Create genre",
  description="Creates a new genre and returns it.",
)
async def create_genre(data: dtos.GenreRequest, db: AsyncSession = Depends(get_db), _: dict = Depends(require_admin)):
  return await service.create(db, data)


# UPDATE ----------------------------------------------------------
@router.put(
  "/{id}",
  response_model=dtos.GenreResponse,
  status_code=HTTP_200_OK,
  summary="Update genre",
  description="Updates a genre by its ID. Raises 404 if not found.",
)
async def update_genre(
  id: int,
  data: dtos.GenreRequest,
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  genre = await service.update(db, id, data)

  return genre


# DELETE ----------------------------------------------------------
@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete genre",
  description="Deletes a genre by its ID. Raises 404 if not found.",
)
async def delete_genre(
  id: int,
  db: AsyncSession = Depends(get_db),
  _: dict = Depends(require_admin),
):
  await service.delete(db, id)
