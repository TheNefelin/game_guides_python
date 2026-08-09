from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.dependencies import verify_api_key, require_user
from src.core.database import get_db
from src.core.limiter import limiter
from . import schemas, service

router = APIRouter(
  prefix="/contact",
  tags=["contact"],
  dependencies=[Depends(verify_api_key)],
)


def get_user_id(payload: dict = Depends(require_user)) -> UUID:
  return UUID(payload["sub"])


@router.post(
  "/",
  response_model=schemas.ContactResponse,
  status_code=HTTP_200_OK,
  summary="Send contact message",
  description="Sends a contact message from the authenticated user via email.",
)
@limiter.limit("5/minute")
async def send_contact(
  request: Request,
  data: schemas.ContactRequest,
  user_id: UUID = Depends(get_user_id),
  db: AsyncSession = Depends(get_db),
):
  return await service.send_contact(db, user_id, data)
