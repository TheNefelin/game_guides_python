from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import NotFoundError
from . import repository


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: UUID) -> dtos.UserResponse:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("User")

  return dtos.UserResponse.model_validate(entity)


# GET OR CREATE USER (Auth) ---------------------------------------
async def get_or_create_user(db: AsyncSession, email: str) -> dtos.UserResponse:
  entity = await repository.get_by_email(db, email)

  if not entity:
    entity = await repository.create(db, {"email": email, "role_id": 1})

  return dtos.UserResponse.model_validate(entity)
