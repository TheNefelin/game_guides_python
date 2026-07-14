import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from src.api.users import service as users_service
from src.core import security
from src.core.exceptions import UnauthorizedError

from . import schemas, google_service, session_repository

REFRESH_TOKEN_DAYS = 7


def auth_service(db: Session, google_token: str) -> schemas.AuthGoogleResponse:
  google_user_info = google_service.verify_google_token(google_token)

  if not google_user_info.email_verified:
    raise UnauthorizedError(message="Email not verified")

  user = users_service.get_or_create_user(db, google_user_info.email)

  token = security.create_access_token(
    user.id,
    user.role.name
  )

  refresh_token = secrets.token_urlsafe(32)
  expires_at = datetime.now(tz=timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS)
  session_repository.create(db, user.id, refresh_token, expires_at)

  auth_user = schemas.AuthGoogleUser (
    id_user = str(user.id),
    email = user.email,
    name = google_user_info.name,
    picture = google_user_info.picture,
    role = user.role.name
  )

  return schemas.AuthGoogleResponse(
    token=token,
    refresh_token=refresh_token,
    user=auth_user
  )


def refresh_session(db: Session, refresh_token: str) -> schemas.AuthRefreshResponse:
  session = session_repository.get_by_token(db, refresh_token)

  if not session or session.is_revoked or session.expires_at < datetime.now(tz=timezone.utc):
    raise UnauthorizedError("Invalid or expired refresh token")

  session_repository.revoke(db, session)

  new_refresh = secrets.token_urlsafe(32)
  expires_at = datetime.now(tz=timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS)
  session_repository.create(db, session.user_id, new_refresh, expires_at)

  token = security.create_access_token(session.user_id, session.user.role.name)
  return schemas.AuthRefreshResponse(token=token, refresh_token=new_refresh)


def revoke_session(db: Session, refresh_token: str) -> None:
  session = session_repository.get_by_token(db, refresh_token)

  if not session:
    raise UnauthorizedError("Invalid refresh token")

  session_repository.revoke(db, session)
