from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/genres",
  tags=["genres"],
)


# GET ALL ---------------------------------------------------------
@router.get(
  "/",
  response_model=dtos.PaginationResponse[dtos.GenreResponse],
  status_code=HTTP_200_OK,
  summary="Get all genres",
  description="Returns a paginated list of genres ordered by name.",
)
def get_all_genres(
  page: int = 1,
  limit: int = 20,
  db: Session = Depends(get_db),
):
  return service.get_all(db, page, limit)


# GET BY ID -------------------------------------------------------
@router.get(
  "/{id}",
  response_model=dtos.GenreResponse,
  status_code=HTTP_200_OK,
  summary="Get genre by ID",
  description="Returns a genre by its ID. Raises 404 if not found.",
)
def get_genre_by_id(id: int, db: Session = Depends(get_db)):
  genre = service.get_by_id(db, id)

  if not genre:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Genre not found")

  return genre


# CREATE ----------------------------------------------------------
@router.post(
  "/",
  response_model=dtos.GenreResponse,
  status_code=HTTP_201_CREATED,
  summary="Create genre",
  description="Creates a new genre and returns it.",
)
def create_genre(data: dtos.GenreRequest, db: Session = Depends(get_db)):
  return service.create(db, data)


# UPDATE ----------------------------------------------------------
@router.put(
  "/{id}",
  response_model=dtos.GenreResponse,
  status_code=HTTP_200_OK,
  summary="Update genre",
  description="Updates a genre by its ID. Raises 404 if not found.",
)
def update_genre(
  id: int, 
  data: dtos.GenreRequest, 
  db: Session = Depends(get_db)
):
  genre = service.update(db, id, data)

  if not genre:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Genre not found")

  return genre


# DELETE ----------------------------------------------------------
@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Delete genre",
  description="Deletes a genre by its ID. Raises 404 if not found.",
)
def delete_genre(
  id: int, 
  db: Session = Depends(get_db)
):
  deleted = service.delete(db, id)

  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Genre not found")
