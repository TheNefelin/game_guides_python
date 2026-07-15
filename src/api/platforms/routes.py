from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/platforms",
  tags=["platforms"],
  dependencies=[Depends(verify_api_key)],
)


# GET ALL ---------------------------------------------------------
@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.PlatformsResponse],
  status_code=HTTP_200_OK,
  summary="Get all platforms",
  description="Returns a paginated list of platforms ordered by name.",
)
async def get_platforms(
  page: int = 1,
  limit: int = 20,
  db: AsyncSession = Depends(get_db),
):
  return await service.get_all(db, page, limit)


# GET BY ID -------------------------------------------------------
@router.get(
  "/{id}",
  response_model=dtos.PlatformsResponse,
  status_code=HTTP_200_OK,
  summary="Get platform by ID",
  description="Returns a platform by its ID. Raises 404 if not found.",
)
async def get_platform_by_id(id: int, db: AsyncSession = Depends(get_db)):
  platform = await service.get_by_id(db, id)

  if not platform:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Platform not found")

  return platform


# CREATE ----------------------------------------------------------
@router.post(
  "/",
  response_model=dtos.PlatformsResponse,
  status_code=HTTP_201_CREATED,
  summary="Create platform",
  description="Creates a new platform and returns it.",
)
async def create_platform(data: dtos.PlatformsRequest, db: AsyncSession = Depends(get_db)):
  return await service.create(db, data)


# UPDATE ----------------------------------------------------------
@router.put(
  "/{id}",
  response_model=dtos.PlatformsResponse,
  status_code=HTTP_200_OK,
  summary="Update platform",
  description="Updates a platform by its ID. Raises 404 if not found.",
)
async def update_platform(id: int, data: dtos.PlatformsRequest, db: AsyncSession = Depends(get_db)):
  platform = await service.update(db, id, data)

  if not platform:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Platform not found")

  return platform


# DELETE ----------------------------------------------------------
@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete platform",
  description="Deletes a platform by its ID. Raises 404 if not found.",
)
async def delete_platform(id: int, db: AsyncSession = Depends(get_db)):
  deleted = await service.delete(db, id)

  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Platform not found")
