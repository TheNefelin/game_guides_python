from sqlalchemy.ext.asyncio import AsyncSession

from src.api.roles import repository
from src.schemas import dtos


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> dtos.RoleResponse | None:
  entity = await repository.get_by_id(db, id)

  if not entity:
    return None

  return dtos.RoleResponse.model_validate(entity)
