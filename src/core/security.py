from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from uuid import UUID

from src.core.config import settings
from src.core.exceptions import ForbiddenError, UnauthorizedError

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def create_access_token(user_id: UUID, role: str) -> str:
  now = datetime.now(tz=timezone.utc)
  expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  payload = {
    "sub": str(user_id),
    "role": role,
    "exp": expire,
    "iat": now
  }

  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except JWTError:
    raise UnauthorizedError()


def get_current_user(required_roles: Optional[List[str]] = None):
  def _get_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if required_roles is not None:
      role = payload.get("role")

      if role not in required_roles:
        raise ForbiddenError()

    return payload
  return _get_user
