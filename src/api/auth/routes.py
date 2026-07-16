from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.core.dependencies import verify_api_key
from src.core import database
from src.core.limiter import limiter
from . import schemas, service

router = APIRouter(
  prefix="/auth", 
  tags=["auth"],
  dependencies=[Depends(verify_api_key)],
)


@router.post(
  "/google",
  response_model=schemas.AuthGoogleResponse,
  status_code=HTTP_200_OK,
  summary="Authenticate with Google",
  description="Validates Google token, gets/creates user and returns JWT.",
)
@limiter.limit("10/minute")
async def auth_google(
  request: Request,
  auth_data: schemas.AuthGoogleRequest,
  db: AsyncSession = Depends(database.get_db)
):
  return await service.auth_service(db, auth_data.googleToken)


@router.post(
  "/refresh",
  response_model=schemas.AuthRefreshResponse,
  status_code=HTTP_200_OK,
  summary="Refresh JWT token",
  description="Rotates refresh token and returns new JWT + new refresh token.",
)
async def auth_refresh(
  data: schemas.AuthRefreshRequest,
  db: AsyncSession = Depends(database.get_db)
):
  return await service.refresh_session(db, data.refresh_token)


@router.post(
  "/logout",
  status_code=HTTP_204_NO_CONTENT,
  summary="Logout",
  description="Revokes the refresh token.",
)
async def auth_logout(
  data: schemas.AuthRefreshRequest,
  db: AsyncSession = Depends(database.get_db)
):
  await service.revoke_session(db, data.refresh_token)
