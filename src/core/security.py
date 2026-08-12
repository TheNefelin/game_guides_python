from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.api.users import repository as users_repository
from src.core.config import settings
from src.core.database import get_db
from src.core.exceptions import ForbiddenError, UnauthorizedError

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2
oauth2_scheme = HTTPBearer(auto_error=False)


# CREATE ACCESS TOKEN (JWT firmado HS256) ----------------------------
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


# VERIFY TOKEN (decodifica y valida firma/exp) -----------------------
def verify_token(token: str) -> dict:
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except JWTError:
    raise UnauthorizedError()


# LOAD USER ROLE (lee el rol real desde la BD) -----------------------
async def _load_user_role(db, user_id: UUID) -> str | None:
  return await users_repository.get_role_name_by_id(db, user_id)


# GET CURRENT USER (dependency: user desde token + rol en BD) --------
def get_current_user(required_roles: Optional[List[str]] = None):
  async def _get_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
  ):
    if credentials is None:
      raise UnauthorizedError()

    payload = verify_token(credentials.credentials)

    # El token solo prueba QUÉN es el usuario; el rol REAL se lee de la BD.
    # Así un cambio de rol (o un user eliminado) se refleja de inmediato,
    # sin esperar a que expire el token (2h). User eliminado → 401 (el
    # frontend fuerza logout). Rol insuficiente → 403.
    try:
      user_id = UUID(payload["sub"])
    except (ValueError, KeyError, TypeError):
      raise UnauthorizedError()

    role = await users_repository.get_role_name_by_id(db, user_id)
    if role is None:
      raise UnauthorizedError(message="User no longer exists")

    if required_roles is not None and role not in required_roles:
      raise ForbiddenError()

    payload["role"] = role
    return payload
  return _get_user
