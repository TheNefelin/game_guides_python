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
async def get_or_create_user(db: AsyncSession, email: str, google_id: str) -> dtos.UserResponse:
  # Identidad primaria por google_sub (estable e inmutable). El email puede
  # cambiar en Google y ya no es clave de identidad segura.
  entity = await repository.get_by_google_sub(db, google_id)

  if not entity:
    entity = await repository.get_by_email(db, email)

  if not entity:
    entity = await repository.create(db, {"email": email, "role_id": 1, "google_sub": google_id})
  elif entity.google_sub != google_id or entity.email != email:
    # Sync de identidad: backfill de google_sub (usuario pre-existente) o
    # email actualizado (el usuario lo cambió en Google).
    entity = await repository.update(db, entity, {"google_sub": google_id, "email": email})

  return dtos.UserResponse.model_validate(entity)
