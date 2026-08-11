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
    "description": "A game for testing",
  })
  return response.json()


async def test_create_character(client):
  game = await _create_game(client)
  response = await client.post("/api/characters/", json={
    "game_id": game["id"],
    "name": "Serge",
    "slug": "serge",
  })
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == "Serge"
  assert data["slug"] == "serge"
  assert data["game_id"] == game["id"]
  assert data["is_playable"] is True
  assert "id" in data


async def test_create_character_duplicate_name(client):
  game = await _create_game(client)
  await client.post("/api/characters/", json={"game_id": game["id"], "name": "Kid", "slug": "kid"})
  response = await client.post("/api/characters/", json={"game_id": game["id"], "name": "Kid", "slug": "kid-2"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_create_character_duplicate_slug(client):
  game = await _create_game(client)
  await client.post("/api/characters/", json={"game_id": game["id"], "name": "Kid", "slug": "kid"})
  response = await client.post("/api/characters/", json={"game_id": game["id"], "name": "Kid 2", "slug": "kid"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_get_all_characters_empty(client):
  response = await client.get("/api/characters/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0


async def test_get_all_characters(client):
  game = await _create_game(client)
  await client.post("/api/characters/", json={"game_id": game["id"], "name": "Harle", "slug": "harle"})
  await client.post("/api/characters/", json={"game_id": game["id"], "name": "Lynx", "slug": "lynx"})
  response = await client.get("/api/characters/")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 2


async def test_get_characters_filter_by_game(client):
  game1 = await _create_game(client)
  game2 = (await client.post("/api/games/", json={"name": "Other Game", "slug": "other-game"})).json()
  await client.post("/api/characters/", json={"game_id": game1["id"], "name": "Serge", "slug": "serge"})
  await client.post("/api/characters/", json={"game_id": game2["id"], "name": "Other", "slug": "other"})
  response = await client.get(f"/api/characters/?game_id={game1['id']}")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 1
  assert data["items"][0]["name"] == "Serge"


async def test_get_character_by_id(client):
  game = await _create_game(client)
  created = (await client.post("/api/characters/", json={"game_id": game["id"], "name": "Serge", "slug": "serge"})).json()
  response = await client.get(f"/api/characters/{created['id']}")
  assert response.status_code == 200
  assert response.json()["name"] == "Serge"


async def test_get_character_by_id_not_found(client):
  response = await client.get("/api/characters/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Character not found"


async def test_update_character(client):
  game = await _create_game(client)
  created = (await client.post("/api/characters/", json={"game_id": game["id"], "name": "Serge", "slug": "serge"})).json()
  response = await client.put(f"/api/characters/{created['id']}", json={"game_id": game["id"], "name": "Serge Updated", "slug": "serge-updated"})
  assert response.status_code == 200
  assert response.json()["name"] == "Serge Updated"
  assert response.json()["slug"] == "serge-updated"


async def test_update_character_not_found(client):
  game = await _create_game(client)
  response = await client.put("/api/characters/9999", json={"game_id": game["id"], "name": "Nope", "slug": "nope"})
  assert response.status_code == 404


async def test_update_character_duplicate_name(client):
  game = await _create_game(client)
  await client.post("/api/characters/", json={"game_id": game["id"], "name": "Kid", "slug": "kid"})
  created = (await client.post("/api/characters/", json={"game_id": game["id"], "name": "Harle", "slug": "harle"})).json()
  response = await client.put(f"/api/characters/{created['id']}", json={"game_id": game["id"], "name": "Kid", "slug": "harle"})
  assert response.status_code == 400


async def test_delete_character(client):
  game = await _create_game(client)
  created = (await client.post("/api/characters/", json={"game_id": game["id"], "name": "Serge", "slug": "serge"})).json()
  response = await client.delete(f"/api/characters/{created['id']}")
  assert response.status_code == 204


async def test_delete_character_not_found(client):
  response = await client.delete("/api/characters/9999")
  assert response.status_code == 404


# UPLOAD / DELETE IMAGE -------------------------------------------

IMAGE_URL = "https://res.cloudinary.com/demo/image/upload/v1/characters/serge.webp"
NEW_IMAGE_URL = "https://res.cloudinary.com/demo/image/upload/v2/characters/serge-new.webp"


async def _create_character(client) -> dict:
  game = await _create_game(client)
  response = await client.post("/api/characters/", json={
    "game_id": game["id"],
    "name": "Serge",
    "slug": "serge",
  })
  return response.json()


async def test_upload_character_image(client):
  character = await _create_character(client)
  with patch("src.api.characters.service.upload_image_1_1", return_value=(IMAGE_URL, "characters/serge")):
    response = await client.post(
      "/api/characters/upload-image",
      data={"id": str(character["id"])},
      files={"file": ("serge.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 200
  assert response.json()["image_url"] == IMAGE_URL


async def test_upload_character_image_replaces_old_image(client):
  character = await _create_character(client)
  with patch("src.api.characters.service.upload_image_1_1", return_value=(IMAGE_URL, "characters/serge")):
    await client.post(
      "/api/characters/upload-image",
      data={"id": str(character["id"])},
      files={"file": ("serge.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.characters.service.upload_image_1_1", return_value=(NEW_IMAGE_URL, "characters/serge-new")), \
       patch("src.api.characters.service.cloudinary_delete") as mock_delete:
    response = await client.post(
      "/api/characters/upload-image",
      data={"id": str(character["id"])},
      files={"file": ("serge.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 200
  mock_delete.assert_called_once_with("characters/serge")


async def test_upload_character_image_keeps_old_on_upload_failure(client):
  import pytest
  character = await _create_character(client)
  with patch("src.api.characters.service.upload_image_1_1", return_value=(IMAGE_URL, "characters/serge")):
    await client.post(
      "/api/characters/upload-image",
      data={"id": str(character["id"])},
      files={"file": ("serge.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.characters.service.upload_image_1_1", side_effect=RuntimeError("upload failed")) as mock_upload, \
       patch("src.api.characters.service.cloudinary_delete") as mock_delete:
    with pytest.raises(RuntimeError):
      await client.post(
        "/api/characters/upload-image",
        data={"id": str(character["id"])},
        files={"file": ("serge.png", _image_bytes(), "image/png")},
      )
  mock_upload.assert_called_once()
  mock_delete.assert_not_called()


async def test_upload_character_image_unknown_character(client):
  response = await client.post(
    "/api/characters/upload-image",
    data={"id": "9999"},
    files={"file": ("serge.png", _image_bytes(), "image/png")},
  )
  assert response.status_code == 404


async def test_upload_character_image_rejects_non_image(client):
  character = await _create_character(client)
  response = await client.post(
    "/api/characters/upload-image",
    data={"id": str(character["id"])},
    files={"file": ("serge.txt", b"not an image", "text/plain")},
  )
  assert response.status_code == 400


async def test_delete_character_image(client):
  character = await _create_character(client)
  with patch("src.api.characters.service.upload_image_1_1", return_value=(IMAGE_URL, "characters/serge")):
    await client.post(
      "/api/characters/upload-image",
      data={"id": str(character["id"])},
      files={"file": ("serge.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.characters.service.cloudinary_delete") as mock_delete:
    response = await client.delete(f"/api/characters/{character['id']}/image")
  assert response.status_code == 200
  assert response.json()["image_url"] is None
  mock_delete.assert_called_once_with("characters/serge")


async def test_delete_character_image_not_found(client):
  response = await client.delete("/api/characters/9999/image")
  assert response.status_code == 404
