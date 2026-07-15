import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse

from src.core.exceptions import AppError
from src.core.logger import logger
from src.api.auth.routes import router as auth_router
from src.api.platforms.routes import router as platforms_router
from src.api.genres.routes import router as genres_router

app = FastAPI(title="Game Guides API", description="In development", version="1.0")

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
  
@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
  logger.error("Unhandled exception: %s", exc)
  return JSONResponse(status_code=500, content={"detail": "Internal server error"})
    
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:4200",  # Angular
    "http://localhost:4321",  # Astro
  ],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["*"],
)

BASE_DIR = os.getcwd()  # raíz del proyecto
STATIC_PATH = os.path.join(BASE_DIR, "static") 

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  return FileResponse(os.path.join(STATIC_PATH, "favicon.ico"))

@app.get("/")
async def root():
  return {
    "status": "Api Running",
    "swagger": "/docs",
    "version": "v1.1", 
  }

app.include_router(auth_router, prefix="/api")
app.include_router(platforms_router, prefix="/api")
app.include_router(genres_router, prefix="/api")
