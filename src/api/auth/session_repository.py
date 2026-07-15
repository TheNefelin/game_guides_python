import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import models
from src.models.models import UserSession


async def create(db: AsyncSession, user_id: uuid.UUID, refresh_token: str, expires_at: datetime) -> UserSession:
  session = UserSession(user_id=user_id, refresh_token=refresh_token, expires_at=expires_at)
  db.add(session)
  await db.commit()
  await db.refresh(session)
  return session


async def get_by_token(db: AsyncSession, token: str) -> UserSession | None:
  result = await db.execute(
    select(UserSession)
    .options(joinedload(UserSession.user).joinedload(models.User.role))
    .where(UserSession.refresh_token == token)
  )
  return result.scalar_one_or_none()


async def revoke(db: AsyncSession, session: UserSession) -> None:
  session.is_revoked = True
  await db.commit()
