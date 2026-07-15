from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# GET BY ID -------------------------------------------------------
async def get_by_id(db: AsyncSession, id: int) -> models.Role | None:
  result = await db.execute(select(models.Role).where(models.Role.id == id))
  return result.scalar_one_or_none()
