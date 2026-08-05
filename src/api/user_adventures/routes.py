from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key, require_user
from src.core.database import get_db
from src.schemas import dtos
from . import service

router = APIRouter(
  prefix="/user-adventures",
  tags=["user-adventures"],
  dependencies=[Depends(verify_api_key)],
)


def get_user_id(payload: dict = Depends(require_user)) -> UUID:
  return UUID(payload["sub"])


@router.get(
  "/by-guide/{guide_id}",
  response_model=list[dtos.UserAdventureResponse],
  status_code=HTTP_200_OK,
  summary="Get user adventure progress by guide",
  description="Returns the authenticated user's completion status for all adventures of a guide.",
)
async def get_user_adventures_by_guide(
  guide_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_by_guide(db, user_id, guide_id)


@router.get(
  "/by-game/{game_id}",
  response_model=list[dtos.UserAdventureResponse],
  status_code=HTTP_200_OK,
  summary="Get user adventure progress by game",
  description="Returns the authenticated user's completion status for all adventures of a game's guides.",
)
async def get_user_adventures_by_game(
  game_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.get_by_game(db, user_id, game_id)


@router.post(
  "/",
  response_model=dtos.UserAdventureResponse,
  status_code=HTTP_201_CREATED,
  summary="Mark an adventure as completed",
  description="Upserts the authenticated user's progress for an adventure, marking it completed.",
)
async def create_user_adventure(
  data: dtos.UserAdventureRequest,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.create(db, user_id, data.adventure_id)


@router.delete(
  "/{adventure_id}",
  status_code=HTTP_204_NO_CONTENT,
  summary="Unmark an adventure as completed",
  description="Sets the adventure as not completed for the authenticated user.",
)
async def delete_user_adventure(
  adventure_id: int,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  await service.delete(db, user_id, adventure_id)
