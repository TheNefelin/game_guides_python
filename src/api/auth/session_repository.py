import uuid
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from src.models import models
from src.models.models import UserSession


def create(db: Session, user_id: uuid.UUID, refresh_token: str, expires_at: datetime) -> UserSession:
  session = UserSession(user_id=user_id, refresh_token=refresh_token, expires_at=expires_at)
  db.add(session)
  db.commit()
  db.refresh(session)
  return session


def get_by_token(db: Session, token: str) -> UserSession | None:
  return (
    db.query(UserSession)
    .options(joinedload(UserSession.user).joinedload(models.User.role))
    .filter(UserSession.refresh_token == token)
    .first()
  )


def revoke(db: Session, session: UserSession) -> None:
  session.is_revoked = True
  db.commit()
