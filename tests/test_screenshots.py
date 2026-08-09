import io
from unittest.mock import patch

from PIL import Image


def _image_bytes() -> bytes:
  buffer = io.BytesIO()
  Image.new("RGB", (4, 4)).save(buffer, format="PNG")
  return buffer.getvalue()


async def test_create_screenshot(client):
  game = (await client.post("/api/games/", json={"name": "Test Game", "slug": "test-game"})).json()
  with patch("src.api.screenshots.service.upload_image_16_9", return_value=("https://example.com/shot.webp", "screenshots/shot")):
    response = await client.post(
      "/api/screenshots/upload-image",
      data={"game_id": str(game["id"]), "alt_text": "Gameplay", "sort_order": "0"},
      files={"file": ("shot.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 201
  data = response.json()
  assert data["game_id"] == game["id"]
  assert data["image_url"] == "https://example.com/shot.webp"
  assert data["alt_text"] == "Gameplay"


async def test_create_screenshot_unknown_game(client):
  with patch("src.api.screenshots.service.upload_image_16_9", return_value=("https://example.com/shot.webp", "screenshots/shot")):
    response = await client.post(
      "/api/screenshots/upload-image",
      data={"game_id": "9999"},
      files={"file": ("shot.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 400
  assert "does not exist" in response.json()["detail"]


async def test_create_screenshot_rejects_non_image(client):
  game = (await client.post("/api/games/", json={"name": "Test Game", "slug": "test-game"})).json()
  response = await client.post(
    "/api/screenshots/upload-image",
    data={"game_id": str(game["id"])},
    files={"file": ("shot.txt", b"not an image", "text/plain")},
  )
  assert response.status_code == 400


async def test_delete_screenshot(client):
  game = (await client.post("/api/games/", json={"name": "Test Game", "slug": "test-game"})).json()
  with patch("src.api.screenshots.service.upload_image_16_9", return_value=("https://example.com/shot.webp", "screenshots/shot")):
    created = await client.post(
      "/api/screenshots/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("shot.png", _image_bytes(), "image/png")},
    )
  response = await client.delete(f"/api/screenshots/{created.json()['id']}/image")
  assert response.status_code == 204


async def test_delete_screenshot_not_found(client):
  response = await client.delete("/api/screenshots/9999/image")
  assert response.status_code == 404
  assert response.json()["detail"] == "Screenshot not found"
