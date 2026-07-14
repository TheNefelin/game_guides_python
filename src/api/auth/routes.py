from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.core import database
from . import schemas, service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
  "/google",
  response_model=schemas.AuthGoogleResponse,
  status_code=HTTP_200_OK,
  summary="Authenticate with Google",
  description="Validates Google token, gets/creates user and returns JWT.",
)
def auth_google(
  auth_data: schemas.AuthGoogleRequest,
  db: Session = Depends(database.get_db)
):
  return service.auth_service(db, auth_data.googleToken)


@router.post(
  "/refresh",
  response_model=schemas.AuthRefreshResponse,
  status_code=HTTP_200_OK,
  summary="Refresh JWT token",
  description="Rotates refresh token and returns new JWT + new refresh token.",
)
def auth_refresh(
  data: schemas.AuthRefreshRequest,
  db: Session = Depends(database.get_db)
):
  return service.refresh_session(db, data.refresh_token)


@router.post(
  "/logout",
  status_code=HTTP_204_NO_CONTENT,
  summary="Logout",
  description="Revokes the refresh token.",
)
def auth_logout(
  data: schemas.AuthRefreshRequest,
  db: Session = Depends(database.get_db)
):
  service.revoke_session(db, data.refresh_token)
