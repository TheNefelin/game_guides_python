import httpx

from src.core.config import settings
from src.core.exceptions import UnauthorizedError
from . import schemas

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


async def _fetch_userinfo(client: httpx.AsyncClient, access_token: str) -> dict:
  response = await client.get(
    GOOGLE_USERINFO_URL,
    headers={"Authorization": f"Bearer {access_token}"},
  )
  return response.json() if response.status_code == 200 else {}


async def verify_google_token(access_token: str) -> schemas.GoogleUserInfo:
  # Validar el token contra Google y verificar que fue emitido para ESTA
  # aplicación (aud == GOOGLE_CLIENT_ID). Sin este check, cualquier access
  # token de Google válido (emitido a otra app) permitiría autenticarse.
  async with httpx.AsyncClient(timeout=10) as client:
    response = await client.get(
      GOOGLE_TOKEN_INFO_URL,
      params={"access_token": access_token},
    )

  if response.status_code != 200:
    raise UnauthorizedError(message="Invalid Google token")

  token_info = response.json()

  if settings.GOOGLE_CLIENT_ID and token_info.get("aud") != settings.GOOGLE_CLIENT_ID:
    raise UnauthorizedError(message="Invalid Google token")

  # Los access tokens (lo que envía el frontend) no traen `iss` de forma
  # confiable (ese campo solo está garantizado en id_tokens). Solo se exige
  # cuando viene presente; la seguridad real la da el check de `aud`.
  iss = token_info.get("iss")
  if iss and iss not in ("accounts.google.com", "https://accounts.google.com"):
    raise UnauthorizedError(message="Invalid Google token")

  email_verified = token_info.get("email_verified")
  if email_verified not in (True, "true"):
    raise UnauthorizedError(message="Email not verified")

  # /tokeninfo con un access token no garantiza `picture`/`name`. Si faltan,
  # se consultan de /userinfo (misma validez: el token ya fue validado por aud).
  userinfo = {}
  if not token_info.get("picture") or not token_info.get("name"):
    async with httpx.AsyncClient(timeout=10) as client:
      userinfo = await _fetch_userinfo(client, access_token)

  return schemas.GoogleUserInfo(
    google_id=token_info["sub"],
    email=token_info["email"],
    name=userinfo.get("name") or token_info.get("name"),
    picture=userinfo.get("picture") or token_info.get("picture"),
    email_verified=True,
  )
