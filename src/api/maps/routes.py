from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/maps",
  tags=["maps"],
  dependencies=[Depends(verify_api_key)],
)


@router.get(
  "/",
  response_model=list[dtos.MapResponse],
  status_code=HTTP_200_OK,
)
async def get_maps(
  game_id: int = Query(),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_by_game(db, game_id)


@router.post(
  "/",
  response_model=dtos.MapResponse,
  status_code=HTTP_201_CREATED,
)
async def create_map(
  game_id: int = Form(),
  file: UploadFile = File(...),
  alt_text: str | None = Form(default=None),
  db: AsyncSession = Depends(get_db),
):
  return await service.create(db, game_id, await file.read(), alt_text)


@router.delete(
  "/{id}",
  status_code=HTTP_204_NO_CONTENT,
)
async def delete_map(id: int, db: AsyncSession = Depends(get_db)):
  deleted = await service.delete(db, id)
  if not deleted:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Map not found")
