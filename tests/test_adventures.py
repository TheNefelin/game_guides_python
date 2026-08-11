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


async def _create_adventure(client, guide_id: int, **overrides) -> dict:
  payload = {"guide_id": guide_id, "description": "Travel to the past"}
  payload.update(overrides)
  response = await client.post("/api/adventures/", json=payload)
  return response.json()


async def test_create_adventure(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  response = await client.post("/api/adventures/", json={
    "guide_id": guide["id"],
    "description": "Travel to 1000 A.D.",
    "is_important": True,
  })
  assert response.status_code == 201
  data = response.json()
  assert data["description"] == "Travel to 1000 A.D."
  assert data["guide_id"] == guide["id"]
  assert data["is_important"] is True
  assert "id" in data


async def test_create_adventure_unknown_guide(client):
  response = await client.post("/api/adventures/", json={"guide_id": 9999, "description": "Nope"})
  assert response.status_code == 400
  assert "does not exist" in response.json()["detail"]


async def test_get_all_adventures_empty(client):
  response = await client.get("/api/adventures/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0


async def test_get_all_adventures(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  await _create_adventure(client, guide["id"])
  await _create_adventure(client, guide["id"], description="Another step")
  response = await client.get("/api/adventures/")
  assert response.status_code == 200
  assert response.json()["total"] == 2


async def test_get_adventures_filter_by_guide(client):
  game = await _create_game(client)
  guide1 = await _create_guide(client, game["id"])
  guide2 = (await client.post("/api/guides/", json={"game_id": game["id"], "title": "Other"})).json()
  await _create_adventure(client, guide1["id"])
  await _create_adventure(client, guide2["id"], description="Other step")
  response = await client.get(f"/api/adventures/?guide_id={guide1['id']}")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 1
  assert data["items"][0]["description"] == "Travel to the past"


async def test_get_adventure_by_id(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  created = await _create_adventure(client, guide["id"])
  response = await client.get(f"/api/adventures/{created['id']}")
  assert response.status_code == 200
  assert response.json()["description"] == "Travel to the past"


async def test_get_adventure_by_id_not_found(client):
  response = await client.get("/api/adventures/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Adventure not found"


async def test_update_adventure(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  created = await _create_adventure(client, guide["id"])
  response = await client.put(f"/api/adventures/{created['id']}", json={
    "guide_id": guide["id"],
    "description": "Updated step",
  })
  assert response.status_code == 200
  assert response.json()["description"] == "Updated step"


async def test_update_adventure_not_found(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  response = await client.put("/api/adventures/9999", json={"guide_id": guide["id"], "description": "Nope"})
  assert response.status_code == 404


async def test_delete_adventure(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  created = await _create_adventure(client, guide["id"])
  response = await client.delete(f"/api/adventures/{created['id']}")
  assert response.status_code == 204


async def test_delete_adventure_not_found(client):
  response = await client.delete("/api/adventures/9999")
  assert response.status_code == 404


async def test_delete_adventure_with_user_progress_blocked(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})
  response = await client.delete(f"/api/adventures/{adventure['id']}")
  assert response.status_code == 400
  assert "user progress (1)" in response.json()["detail"]


async def test_delete_adventure_cleans_cloudinary_images(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  with patch("src.api.adventure_images.service.upload_image_16_9", return_value=("https://res.cloudinary.com/demo/image/upload/v1/adventures/img.webp", "adventures/img")):
    created = await client.post(
      "/api/adventure-images/upload-image",
      data={"adventure_id": str(adventure["id"])},
      files={"file": ("img.png", _image_bytes(), "image/png")},
    )
  assert created.status_code == 201
  with patch("src.api.adventures.service.cloudinary_delete") as mock_delete:
    response = await client.delete(f"/api/adventures/{adventure['id']}")
  assert response.status_code == 204
  mock_delete.assert_called_once_with("adventures/img")
