from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from . import repository


# GET BY GAME ------------------------------------------------------
async def get_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> dtos.UserProgressResponse:
  guides = await repository.get_guides_by_game(db, user_id, game_id)
  adventures = await repository.get_adventures_by_game(db, user_id, game_id)
  return dtos.UserProgressResponse(
    guides=[dtos.UserGuideResponse.model_validate(g) for g in guides],
    adventures=[dtos.UserAdventureResponse.model_validate(a) for a in adventures],
  )


# DELETE BY GAME (resetea progreso del juego) -----------------------
async def delete_by_game(db: AsyncSession, user_id: UUID, game_id: int) -> None:
  await repository.delete_by_game(db, user_id, game_id)
