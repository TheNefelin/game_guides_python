import io
from unittest.mock import patch

from PIL import Image


def _image_bytes() -> bytes:
  buffer = io.BytesIO()
  Image.new("RGB", (4, 4)).save(buffer, format="PNG")
  return buffer.getvalue()


async def test_create_map(client):
  game = (await client.post("/api/games/", json={"name": "Test Game", "slug": "test-game"})).json()
  with patch("src.api.maps.service.upload_image_free", return_value=("https://example.com/map.webp", "maps/map")):
    response = await client.post(
      "/api/maps/upload-image",
      data={"game_id": str(game["id"]), "alt_text": "World map", "sort_order": "1"},
      files={"file": ("map.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 201
  data = response.json()
  assert data["game_id"] == game["id"]
  assert data["image_url"] == "https://example.com/map.webp"
  assert data["alt_text"] == "World map"
  assert data["sort_order"] == 1


async def test_create_map_unknown_game(client):
  with patch("src.api.maps.service.upload_image_free", return_value=("https://example.com/map.webp", "maps/map")):
    response = await client.post(
      "/api/maps/upload-image",
      data={"game_id": "9999"},
      files={"file": ("map.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 400
  assert "does not exist" in response.json()["detail"]


async def test_create_map_rejects_non_image(client):
  game = (await client.post("/api/games/", json={"name": "Test Game", "slug": "test-game"})).json()
  response = await client.post(
    "/api/maps/upload-image",
    data={"game_id": str(game["id"])},
    files={"file": ("map.txt", b"not an image", "text/plain")},
  )
  assert response.status_code == 400


async def test_delete_map(client):
  game = (await client.post("/api/games/", json={"name": "Test Game", "slug": "test-game"})).json()
  with patch("src.api.maps.service.upload_image_free", return_value=("https://example.com/map.webp", "maps/map")):
    created = await client.post(
      "/api/maps/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("map.png", _image_bytes(), "image/png")},
    )
  response = await client.delete(f"/api/maps/{created.json()['id']}/image")
  assert response.status_code == 204


async def test_delete_map_not_found(client):
  response = await client.delete("/api/maps/9999/image")
  assert response.status_code == 404
  assert response.json()["detail"] == "Map not found"
