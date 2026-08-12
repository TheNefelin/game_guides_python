import os
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse

from fastapi_problem.handler import add_exception_handler, new_exception_handler
from rfc9457 import BadRequestProblem, Problem, ServerProblem, UnprocessableProblem
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.core.config import settings
from src.core.limiter import limiter
from src.core.logger import logger, set_request_id
from src.api.auth.routes import router as auth_router
from src.api.platforms.routes import router as platforms_router
from src.api.genres.routes import router as genres_router
from src.api.games.routes import router as games_router
from src.api.characters.routes import router as characters_router
from src.api.sources.routes import router as sources_router
from src.api.screenshots.routes import router as screenshots_router
from src.api.maps.routes import router as maps_router
from src.api.guides.routes import router as guides_router
from src.api.adventures.routes import router as adventures_router
from src.api.adventure_images.routes import router as adventure_images_router
from src.api.user_guides.routes import router as user_guides_router
from src.api.user_adventures.routes import router as user_adventures_router
from src.api.user_progress.routes import router as user_progress_router
from src.api.contact.routes import router as contact_router

start_time = time.time()

app = FastAPI(title="Game Guides API", description="In development", version="1.0")
app.state.limiter = limiter


# LOGGING MIDDLEWARE (request_id + duración por request) ---------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
  request_id = str(uuid.uuid4())
  set_request_id(request_id)
  start = time.time()
  response = await call_next(request)
  duration = round((time.time() - start) * 1000, 2)
  logger.info("%s %s", request.method, request.url.path, extra={
    "props": {
      "method": request.method,
      "path": request.url.path,
      "status_code": response.status_code,
      "duration_ms": duration,
    }
  })
  return response

# PROBLEM HANDLERS (respuestas RFC 9457) ------------------------------
class RequestValidationProblem(UnprocessableProblem):
  type_ = "request-validation-failed"
  title = "Request validation error."

  def __init__(self, errors=None, **kwargs):
    super().__init__(errors=errors, **kwargs)
    self.detail = "; ".join(str(e.get("msg", "")) for e in errors) if errors else self.title


class InternalServerErrorProblem(ServerProblem):
  type_ = "internal-server-error"
  title = "Internal server error."

  def __init__(self, detail=None, **kwargs):
    super().__init__(detail="Internal server error", **kwargs)


class RateLimitProblem(BadRequestProblem):
  type_ = "rate-limit-exceeded"
  title = "Rate limit exceeded."
  status = 429


# RATE LIMIT HANDLER (mapea RateLimitExceeded) -------------------------
def rate_limit_handler(eh, request: Request, exc: RateLimitExceeded):
  headers = None
  if hasattr(request.state, "view_rate_limit"):
    response = request.app.state.limiter._inject_headers(
      JSONResponse({}), request.state.view_rate_limit
    )
    headers = dict(response.headers)
  return RateLimitProblem(detail=f"Rate limit exceeded: {exc.detail}", headers=headers)


# LOG PROBLEM (warn en problemas < 500) --------------------------------
def log_problem(request: Request, exc: Exception):
  if isinstance(exc, Problem) and exc.status < 500:
    logger.warning("%s: %s", exc.title, exc.detail, extra={
      "props": {"status_code": exc.status}
    })


eh = new_exception_handler(
  logger=logger,
  unhandled_wrappers={
    "422": RequestValidationProblem,
    "500": InternalServerErrorProblem,
  },
  handlers={RateLimitExceeded: rate_limit_handler},
  pre_hooks=[log_problem],
)
add_exception_handler(app, eh)
app.add_exception_handler(RateLimitExceeded, eh)

# MIDDLEWARES ---------------------------------------------------------
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.cors_origins_list,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["*"],
)


# STATIC FILES --------------------------------------------------------
BASE_DIR = os.getcwd()  # raíz del proyecto
STATIC_PATH = os.path.join(BASE_DIR, "static") 

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")


# HEALTH / FAVICON ----------------------------------------------------
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  return FileResponse(os.path.join(STATIC_PATH, "favicon.ico"))

@app.get("/health")
@limiter.exempt
async def health():
  return {
    "status": "ok",
    "version": "v1.1",
    "uptime_seconds": round(time.time() - start_time, 2),
  }


# ROUTERS -------------------------------------------------------------
app.include_router(auth_router, prefix="/api")
app.include_router(platforms_router, prefix="/api")
app.include_router(genres_router, prefix="/api")
app.include_router(games_router, prefix="/api")
app.include_router(characters_router, prefix="/api")
app.include_router(sources_router, prefix="/api")
app.include_router(screenshots_router, prefix="/api")
app.include_router(maps_router, prefix="/api")
app.include_router(guides_router, prefix="/api")
app.include_router(adventures_router, prefix="/api")
app.include_router(adventure_images_router, prefix="/api")
app.include_router(user_guides_router, prefix="/api")
app.include_router(user_adventures_router, prefix="/api")
app.include_router(user_progress_router, prefix="/api")
app.include_router(contact_router, prefix="/api")
