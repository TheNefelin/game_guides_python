import uuid
from unittest.mock import AsyncMock, patch

import pytest

from src.api.contact import brevo
from src.core.security import create_access_token
from src.models.models import User


async def _user_token(user_id: uuid.UUID, role: str = "user") -> str:
  return create_access_token(user_id, role)


async def _create_user(db, email: str = "contact@user.com") -> User:
  user = User(id=uuid.uuid4(), email=email, role_id=1)
  db.add(user)
  await db.flush()
  return user


# /api/contact -----------------------------------------------------


async def test_send_contact_success(client, db):
  user = await _create_user(db)
  token = await _user_token(user.id)

  with patch("src.api.contact.brevo.send_contact_email") as mock_send, patch("src.api.contact.brevo.send_confirmation_email") as mock_confirmation:
    response = await client.post(
      "/api/contact/",
      headers={"Authorization": f"Bearer {token}"},
      json={"reason": "sugerencia", "name": "Test User", "message": "Hola!"},
    )

  assert response.status_code == 200
  assert response.json()["status"] == "sent"
  mock_send.assert_awaited_once()
  assert mock_send.call_args.kwargs["reply_to_email"] == user.email
  mock_confirmation.assert_awaited_once()
  assert mock_confirmation.call_args.args[0] == user.email


async def test_send_contact_user_not_found(client, db):
  token = await _user_token(uuid.uuid4())

  response = await client.post(
    "/api/contact/",
    headers={"Authorization": f"Bearer {token}"},
    json={"reason": "otros", "name": "Ghost", "message": "nadie"},
  )

  assert response.status_code == 401


async def test_send_contact_brevo_failure(client, db):
  user = await _create_user(db)
  token = await _user_token(user.id)

  from src.core.exceptions import AppError

  with patch(
    "src.api.contact.brevo.send_contact_email",
    side_effect=AppError(message="Could not send contact email", status_code=502),
  ):
    response = await client.post(
      "/api/contact/",
      headers={"Authorization": f"Bearer {token}"},
      json={"reason": "reclamo", "name": "Test User", "message": "reclamo"},
    )

  assert response.status_code == 502


async def test_send_contact_email_includes_reply_to():
  payload_captured = {}

  async def fake_send(to_email, to_name, subject, html, reply_to=None):
    payload_captured["to_email"] = to_email
    payload_captured["subject"] = subject
    payload_captured["html"] = html
    payload_captured["reply_to"] = reply_to

  with patch("src.api.contact.brevo._send_email", new=fake_send):
    await brevo.send_contact_email(
      reply_to_email="sender@example.com",
      reply_to_name="Sender Name",
      reason="sugerencia",
      message="Mi mensaje",
    )

  assert payload_captured["to_email"] == brevo.settings.BREVO_FROM_EMAIL
  assert payload_captured["reply_to"] == ("sender@example.com", "Sender Name")
  assert "sender@example.com" in payload_captured["html"]
  assert "Sender Name" in payload_captured["html"]
  assert "sugerencia" in payload_captured["subject"]


async def test_raise_brevo_error_auth():
  from src.core.exceptions import AppError

  with pytest.raises(AppError) as exc_info:
    brevo._raise_brevo_error(401)
  assert exc_info.value.status == 500
  assert "API key" in exc_info.value.detail


async def test_raise_brevo_error_rate_limit():
  from src.core.exceptions import AppError

  with pytest.raises(AppError) as exc_info:
    brevo._raise_brevo_error(429)
  assert exc_info.value.status == 429


async def test_raise_brevo_error_provider():
  from src.core.exceptions import AppError

  with pytest.raises(AppError) as exc_info:
    brevo._raise_brevo_error(500)
  assert exc_info.value.status == 502
