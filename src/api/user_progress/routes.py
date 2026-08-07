from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_user
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/user-progress",
  tags=["user-progress"],
  dependencies=[Depends(verify_api_key)],
)


def get_user_id(payload: dict = Depends(require_user)) -> UUID:
  return UUID(payload["sub"])


@router.get(
  "/by-game/{game_id}",
  response_model=dtos.UserProgressResponse,
  status_code=HTTP_200_OK,
  summary="Get combined user progress by game",
  description="Returns the authenticated user's progress for guides and adventures of a game in a single request.",
)
async def get_user_progress_by_game(
  game_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_by_game(db, user_id, game_id)


@router.delete(
  "/by-game/{game_id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Reset user progress by game",
  description="Unmarks all guides and adventures of a game for the authenticated user.",
)
async def delete_user_progress_by_game(
  game_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  await service.delete_by_game(db, user_id, game_id)
