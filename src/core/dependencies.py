from fastapi import Header

from src.core.config import settings
from src.core.exceptions import InvalidApiKeyError
from src.core.security import get_current_user

# VERIFY API KEY (dependency de X-API-Key) ---------------------------
async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
  if x_api_key != settings.API_KEY:
    raise InvalidApiKeyError()
  return True

# DEPENDENCIAS DE ROL ------------------------------------------------
require_admin = get_current_user(required_roles=["admin"])
require_user = get_current_user()
