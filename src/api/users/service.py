from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from . import repository


# GET OR CREATE USER (Auth) ---------------------------------------
async def get_or_create_user(db: AsyncSession, email: str) -> dtos.UserResponse:
  entity = await repository.get_by_email(db, email)

  if not entity:
    entity = await repository.create(db, {"email": email, "role_id": 1})

  return dtos.UserResponse.model_validate(entity)
