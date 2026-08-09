import pytest

from src.api.contact import brevo
from src.core.config import settings

pytestmark = [
  pytest.mark.live,
  pytest.mark.skipif(
    not settings.TEST_BREVO_EMAIL,
    reason="TEST_BREVO_EMAIL not set",
  ),
]


async def test_send_live_contact_email():
  """Sends a real contact email to TEST_BREVO_EMAIL. Requires a real Brevo API key."""
  await brevo.send_contact_email(
    reply_to_email=settings.TEST_BREVO_EMAIL,
    reply_to_name="Test User",
    reason="sugerencia",
    message="Este es un correo de prueba de integración.",
  )


async def test_send_live_confirmation_email():
  """Sends a real confirmation email to TEST_BREVO_EMAIL."""
  await brevo.send_confirmation_email(settings.TEST_BREVO_EMAIL, "Test User")
