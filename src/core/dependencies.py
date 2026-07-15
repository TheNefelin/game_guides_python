from fastapi import Header

from src.core.config import settings
from src.core.exceptions import InvalidApiKeyError

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
  if x_api_key != settings.API_KEY:
    raise InvalidApiKeyError()
  return True
