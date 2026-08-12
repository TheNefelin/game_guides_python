from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.security import verify_token


# RATE LIMIT KEY (por usuario si hay token, sino por IP) --------------
def rate_limit_key(request: Request) -> str:
  auth_header = request.headers.get("authorization", "")
  if auth_header.lower().startswith("bearer "):
    try:
      payload = verify_token(auth_header.split(" ")[1])
      user_id = payload.get("sub")
      if user_id:
        return f"user:{user_id}"
    except Exception:
      pass
  return get_remote_address(request)


# LIMITER (default: 100 req/min) --------------------------------------
limiter = Limiter(key_func=rate_limit_key, default_limits=["100/minute"])
