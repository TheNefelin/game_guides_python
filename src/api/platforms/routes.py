from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/platforms",
  tags=["platforms"],
)


# GET ALL ---------------------------------------------------------
@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.PlatformsResponse],
  status_code=HTTP_200_OK,
  summary="Get all platforms",
  description="Returns a paginated list of platforms ordered by name.",
)
def get_platforms(
  page: int = 1,
  limit: int = 20,
  db: Session = Depends(get_db),
):
  return service.get_all(db, page, limit)


# GET BY ID -------------------------------------------------------
@router.get(
  "/{id}",
  response_model=dtos.PlatformsResponse,
  status_code=HTTP_200_OK,
  summary="Get platform by ID",
  description="Returns a platform by its ID. Raises 404 if not found.",
)
def get_platform_by_id(id: int, db: Session = Depends(get_db)):
  platform = service.get_by_id(db, id)

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
def create_platform(data: dtos.PlatformsRequest, db: Session = Depends(get_db)):
  return service.create(db, data)


# UPDATE ----------------------------------------------------------
@router.put(
  "/{id}",
  response_model=dtos.PlatformsResponse,
  status_code=HTTP_200_OK,
  summary="Update platform",
  description="Updates a platform by its ID. Raises 404 if not found.",
)
def update_platform(id: int, data: dtos.PlatformsRequest, db: Session = Depends(get_db)):
  platform = service.update(db, id, data)

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
def delete_platform(id: int, db: Session = Depends(get_db)):
  deleted = service.delete(db, id)

  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Platform not found")
