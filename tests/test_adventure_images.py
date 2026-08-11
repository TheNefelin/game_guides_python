import io
from unittest.mock import patch

from PIL import Image


def _image_bytes() -> bytes:
  buffer = io.BytesIO()
  Image.new("RGB", (4, 4)).save(buffer, format="PNG")
  return buffer.getvalue()


async def _create_game(client) -> dict:
  response = await client.post("/api/games/", json={
    "name": "Test Game",
    "slug": "test-game",
  })
  return response.json()


async def _create_guide(client, game_id: int) -> dict:
  response = await client.post("/api/guides/", json={
    "game_id": game_id,
    "title": "Main Story",
  })
  return response.json()


async def _create_adventure(client, guide_id: int) -> dict:
  response = await client.post("/api/adventures/", json={
    "guide_id": guide_id,
    "description": "Travel to the past",
  })
  return response.json()


async def _create_context(client) -> tuple[dict, dict, dict]:
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  return game, guide, adventure


# UPLOAD / DELETE IMAGE -------------------------------------------

IMAGE_URL = "https://res.cloudinary.com/demo/image/upload/v1/adventures/step.webp"


async def test_upload_adventure_image(client):
  _, _, adventure = await _create_context(client)
  with patch("src.api.adventure_images.service.upload_image_16_9", return_value=(IMAGE_URL, "adventures/step")):
    response = await client.post(
      "/api/adventure-images/upload-image",
      data={"adventure_id": str(adventure["id"]), "alt_text": "Map", "sort_order": "1"},
      files={"file": ("step.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 201
  data = response.json()
  assert data["adventure_id"] == adventure["id"]
  assert data["image_url"] == IMAGE_URL
  assert data["alt_text"] == "Map"
  assert data["sort_order"] == 1


async def test_upload_adventure_image_unknown_adventure(client):
  response = await client.post(
    "/api/adventure-images/upload-image",
    data={"adventure_id": "9999"},
    files={"file": ("step.png", _image_bytes(), "image/png")},
  )
  assert response.status_code == 400
  assert "does not exist" in response.json()["detail"]


async def test_upload_adventure_image_rejects_non_image(client):
  _, _, adventure = await _create_context(client)
  response = await client.post(
    "/api/adventure-images/upload-image",
    data={"adventure_id": str(adventure["id"])},
    files={"file": ("step.txt", b"not an image", "text/plain")},
  )
  assert response.status_code == 400


async def test_delete_adventure_image(client):
  _, _, adventure = await _create_context(client)
  with patch("src.api.adventure_images.service.upload_image_16_9", return_value=(IMAGE_URL, "adventures/step")):
    created = await client.post(
      "/api/adventure-images/upload-image",
      data={"adventure_id": str(adventure["id"])},
      files={"file": ("step.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.adventure_images.service.cloudinary_delete") as mock_delete:
    response = await client.delete(f"/api/adventure-images/{created.json()['id']}/image")
  assert response.status_code == 204
  mock_delete.assert_called_once_with("adventures/step")


async def test_delete_adventure_image_not_found(client):
  response = await client.delete("/api/adventure-images/9999/image")
  assert response.status_code == 404
  assert response.json()["detail"] == "Adventure image not found"
