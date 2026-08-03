from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key
from src.core.database import get_db
from src.core.security import get_current_user
from src.schemas import dtos
from . import service

require_user = get_current_user()

router = APIRouter(
  prefix="/user-guides",
  tags=["user-guides"],
  dependencies=[Depends(verify_api_key)],
)


def get_user_id(payload: dict = Depends(require_user)) -> UUID:
  return UUID(payload["sub"])


@router.get(
  "/by-game/{game_id}",
  response_model=list[dtos.UserGuideResponse],
  status_code=HTTP_200_OK,
  summary="Get user guide progress by game",
  description="Returns the authenticated user's completion status for all guides of a game.",
)
async def get_user_guides_by_game(
  game_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_by_game(db, user_id, game_id)


@router.post(
  "/",
  response_model=dtos.UserGuideResponse,
  status_code=HTTP_201_CREATED,
  summary="Mark a guide as completed",
  description="Upserts the authenticated user's progress for a guide, marking it completed.",
)
async def create_user_guide(
  data: dtos.UserGuideRequest,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.create(db, user_id, data.guide_id)


@router.delete(
  "/{guide_id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Unmark a guide as completed",
  description="Sets the guide as not completed for the authenticated user.",
)
async def delete_user_guide(
  guide_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  await service.delete(db, user_id, guide_id)
