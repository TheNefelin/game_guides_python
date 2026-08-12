from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import dtos
from src.core.exceptions import NotFoundError
from src.api.roles import service as roles_service
from . import repository


DEFAULT_ROLE_NAME = "user"


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: UUID) -> dtos.UserResponse:
  entity = await repository.get_by_id(db, id)

  if not entity:
    raise NotFoundError("User")

  return dtos.UserResponse.model_validate(entity)


# GET ROLE NAME BY ID (passthrough para security/deps) -------------
async def get_role_name_by_id(db: AsyncSession, user_id: UUID) -> str | None:
  return await repository.get_role_name_by_id(db, user_id)


# GET OR CREATE USER (Auth) ---------------------------------------
async def get_or_create_user(db: AsyncSession, email: str, google_id: str) -> dtos.UserResponse:
  # Identidad primaria por google_sub (estable e inmutable). El email puede
  # cambiar en Google y ya no es clave de identidad segura.
  entity = await repository.get_by_google_sub(db, google_id)

  if not entity:
    entity = await repository.get_by_email(db, email)

  if not entity:
    role = await roles_service.get_by_name(db, DEFAULT_ROLE_NAME)

    if not role:
      raise NotFoundError("Role")

    entity = await repository.create(db, {"email": email, "role_id": role.id, "google_sub": google_id})
  elif entity.google_sub != google_id or entity.email != email:
    # Sync de identidad: backfill de google_sub (usuario pre-existente) o
    # email actualizado (el usuario lo cambió en Google).
    entity = await repository.update(db, entity, {"google_sub": google_id, "email": email})

  return dtos.UserResponse.model_validate(entity)
