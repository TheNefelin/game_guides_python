from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users import service as users_service
from . import brevo, schemas


# SEND CONTACT (envía correos vía Brevo) ----------------------------
async def send_contact(db: AsyncSession, user_id: UUID, data: schemas.ContactRequest) -> schemas.ContactResponse:
  user = await users_service.get_by_id(db, user_id)

  await brevo.send_contact_email(
    reply_to_email=user.email,
    reply_to_name=data.name,
    reason=data.reason,
    message=data.message,
  )
  await brevo.send_confirmation_email(user.email, data.name)

  return schemas.ContactResponse()
