import io
import uuid
from unittest.mock import patch

from PIL import Image

from src.core.security import create_access_token
from src.models.models import User


def _image_bytes() -> bytes:
  buffer = io.BytesIO()
  Image.new("RGB", (4, 4)).save(buffer, format="PNG")
  return buffer.getvalue()


async def _create_user(db, email: str = "ratelimit@user.com") -> User:
  user = User(id=uuid.uuid4(), email=email, role_id=1)
  db.add(user)
  await db.flush()
  return user


async def _upload_cover(client, game_id: int = 9999):
  return await client.post(
    "/api/games/upload-image",
    data={"game_id": str(game_id)},
    files={"file": ("cover.png", _image_bytes(), "image/png")},
  )


async def test_upload_games_rate_limit_returns_429(client):
  for _ in range(10):
    response = await _upload_cover(client)
    assert response.status_code == 404  # game inexistente, pero el request SÍ cuenta

  response = await _upload_cover(client)
  assert response.status_code == 429
  assert response.json()["type"] == "rate-limit-exceeded"
  assert response.json()["status"] == 429


async def test_upload_games_rate_limit_resets_between_tests(client):
  response = await _upload_cover(client)
  assert response.status_code == 404  # contador nuevo: no queda bloqueado del test anterior


async def test_contact_rate_limit_returns_429(client, db):
  user = await _create_user(db)
  token = create_access_token(user.id, "user")

  async def send():
    return await client.post(
      "/api/contact/",
      headers={"Authorization": f"Bearer {token}"},
      json={"reason": "sugerencia", "name": "Test", "message": "Hola"},
    )

  with patch("src.api.contact.brevo.send_contact_email"), patch("src.api.contact.brevo.send_confirmation_email"):
    for _ in range(5):
      response = await send()
      assert response.status_code == 200

    response = await send()
  assert response.status_code == 429
  assert response.json()["status"] == 429