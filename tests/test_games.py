import io
from unittest.mock import patch

from PIL import Image


def _image_bytes() -> bytes:
  buffer = io.BytesIO()
  Image.new("RGB", (4, 4)).save(buffer, format="PNG")
  return buffer.getvalue()


async def _create_game(client, **overrides) -> dict:
  payload = {
    "name": "Test Game",
    "slug": "test-game",
    "description": "A game for testing",
  }
  payload.update(overrides)
  response = await client.post("/api/games/", json=payload)
  return response.json()


async def test_create_game(client):
  response = await client.post("/api/games/", json={
    "name": "Chrono Trigger",
    "slug": "chrono-trigger",
    "description": "A time-travel RPG",
    "release_year": 1995,
    "rating": 10,
  })
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == "Chrono Trigger"
  assert data["slug"] == "chrono-trigger"
  assert data["release_year"] == 1995
  assert data["rating"] == 10
  assert data["is_enabled"] is True
  assert data["platforms"] == []
  assert data["genres"] == []
  assert "id" in data


async def test_create_game_with_relations(client):
  platform = (await client.post("/api/platforms/", json={"name": "SNES"})).json()
  genre = (await client.post("/api/genres/", json={"name": "RPG"})).json()
  response = await client.post("/api/games/", json={
    "name": "Chrono Trigger",
    "slug": "chrono-trigger",
    "platform_ids": [platform["id"]],
    "genre_ids": [genre["id"]],
  })
  assert response.status_code == 201
  data = response.json()
  assert data["platforms"][0]["name"] == "SNES"
  assert data["genres"][0]["name"] == "RPG"


async def test_create_game_duplicate_name(client):
  await _create_game(client)
  response = await client.post("/api/games/", json={"name": "Test Game", "slug": "other-slug"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_get_all_games_empty(client):
  response = await client.get("/api/games/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0


async def test_get_all_games(client):
  await _create_game(client)
  await _create_game(client, name="Other", slug="other")
  response = await client.get("/api/games/")
  assert response.status_code == 200
  assert response.json()["total"] == 2


async def test_get_games_search(client):
  await _create_game(client)
  await _create_game(client, name="Zelda", slug="zelda")
  response = await client.get("/api/games/?search=zelda")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 1
  assert data["items"][0]["name"] == "Zelda"


async def test_get_game_by_id(client):
  created = await _create_game(client)
  response = await client.get(f"/api/games/{created['id']}")
  assert response.status_code == 200
  assert response.json()["name"] == "Test Game"


async def test_get_game_by_id_not_found(client):
  response = await client.get("/api/games/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Game not found"


async def test_get_game_detail_by_id(client):
  created = await _create_game(client)
  response = await client.get(f"/api/games/{created['id']}/detail")
  assert response.status_code == 200
  data = response.json()
  assert data["screenshots"] == []
  assert data["maps"] == []
  assert data["characters"] == []
  assert data["sources"] == []
  assert data["guides"] == []


async def test_get_game_detail_by_slug(client):
  await _create_game(client)
  response = await client.get("/api/games/by-slug/test-game/detail")
  assert response.status_code == 200
  assert response.json()["name"] == "Test Game"


async def test_get_game_detail_not_found(client):
  response = await client.get("/api/games/9999/detail")
  assert response.status_code == 404


async def test_update_game(client):
  created = await _create_game(client)
  response = await client.put(f"/api/games/{created['id']}", json={
    "name": "Chrono Cross",
    "slug": "chrono-cross",
  })
  assert response.status_code == 200
  assert response.json()["name"] == "Chrono Cross"


async def test_update_game_not_found(client):
  response = await client.put("/api/games/9999", json={"name": "Nope", "slug": "nope"})
  assert response.status_code == 404


async def test_update_game_duplicate_name(client):
  await _create_game(client)
  created = await _create_game(client, name="Other", slug="other")
  response = await client.put(f"/api/games/{created['id']}", json={"name": "Test Game", "slug": "other"})
  assert response.status_code == 400


async def test_create_game_duplicate_slug(client):
  await _create_game(client)
  response = await client.post("/api/games/", json={"name": "Other Game", "slug": "test-game"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_update_game_duplicate_slug(client):
  await _create_game(client)
  created = await _create_game(client, name="Other", slug="other")
  response = await client.put(f"/api/games/{created['id']}", json={"name": "Other", "slug": "test-game"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_create_game_invalid_platform_id(client):
  response = await client.post("/api/games/", json={
    "name": "Broken Game",
    "slug": "broken-game",
    "platform_ids": [9999],
  })
  assert response.status_code == 400
  assert "Invalid references" in response.json()["detail"]


async def test_create_game_invalid_genre_id(client):
  response = await client.post("/api/games/", json={
    "name": "Broken Game",
    "slug": "broken-game",
    "genre_ids": [9999],
  })
  assert response.status_code == 400
  assert "Invalid references" in response.json()["detail"]


async def test_update_game_invalid_platform_id(client):
  created = await _create_game(client)
  response = await client.put(f"/api/games/{created['id']}", json={
    "name": "Test Game",
    "slug": "test-game",
    "platform_ids": [9999],
  })
  assert response.status_code == 400
  assert "Invalid references" in response.json()["detail"]


async def test_delete_game(client):
  created = await _create_game(client)
  response = await client.delete(f"/api/games/{created['id']}")
  assert response.status_code == 204


async def test_delete_game_not_found(client):
  response = await client.delete("/api/games/9999")
  assert response.status_code == 404


async def test_delete_game_with_dependencies(client):
  game = await _create_game(client)
  await client.post("/api/characters/", json={"game_id": game["id"], "name": "Serge", "slug": "serge"})
  response = await client.delete(f"/api/games/{game['id']}")
  assert response.status_code == 400
  assert "dependencies" in response.json()["detail"]


# UPLOAD / DELETE IMAGE -------------------------------------------

COVER_URL = "https://res.cloudinary.com/demo/image/upload/v1/games/cover.webp"
NEW_COVER_URL = "https://res.cloudinary.com/demo/image/upload/v2/games/new.webp"


async def test_upload_game_cover(client):
  game = await _create_game(client)
  with patch("src.api.games.service.cloudinary_upload", return_value=(COVER_URL, "games/cover")):
    response = await client.post(
      "/api/games/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("cover.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 200
  assert response.json()["cover_url"] == COVER_URL


async def test_upload_game_cover_replaces_old_image(client):
  game = await _create_game(client)
  with patch("src.api.games.service.cloudinary_upload", return_value=(COVER_URL, "games/cover")):
    await client.post(
      "/api/games/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("cover.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.games.service.cloudinary_upload", return_value=(NEW_COVER_URL, "games/new")), \
       patch("src.api.games.service.cloudinary_delete") as mock_delete:
    response = await client.post(
      "/api/games/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("cover.png", _image_bytes(), "image/png")},
    )
  assert response.status_code == 200
  mock_delete.assert_called_once_with("games/cover")


async def test_upload_game_cover_keeps_old_on_upload_failure(client):
  import pytest
  game = await _create_game(client)
  with patch("src.api.games.service.cloudinary_upload", return_value=(COVER_URL, "games/cover")):
    await client.post(
      "/api/games/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("cover.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.games.service.cloudinary_upload", side_effect=RuntimeError("upload failed")) as mock_upload, \
       patch("src.api.games.service.cloudinary_delete") as mock_delete:
    with pytest.raises(RuntimeError):
      await client.post(
        "/api/games/upload-image",
        data={"game_id": str(game["id"])},
        files={"file": ("cover.png", _image_bytes(), "image/png")},
      )
  mock_upload.assert_called_once()
  mock_delete.assert_not_called()


async def test_upload_game_cover_unknown_game(client):
  response = await client.post(
    "/api/games/upload-image",
    data={"game_id": "9999"},
    files={"file": ("cover.png", _image_bytes(), "image/png")},
  )
  assert response.status_code == 404


async def test_upload_game_cover_rejects_non_image(client):
  game = await _create_game(client)
  response = await client.post(
    "/api/games/upload-image",
    data={"game_id": str(game["id"])},
    files={"file": ("cover.txt", b"not an image", "text/plain")},
  )
  assert response.status_code == 400


async def test_delete_game_cover(client):
  game = await _create_game(client)
  with patch("src.api.games.service.cloudinary_upload", return_value=(COVER_URL, "games/cover")):
    await client.post(
      "/api/games/upload-image",
      data={"game_id": str(game["id"])},
      files={"file": ("cover.png", _image_bytes(), "image/png")},
    )
  with patch("src.api.games.service.cloudinary_delete") as mock_delete:
    response = await client.delete(f"/api/games/{game['id']}/image")
  assert response.status_code == 200
  assert response.json()["cover_url"] is None
  mock_delete.assert_called_once_with("games/cover")


async def test_delete_game_cover_not_found(client):
  response = await client.delete("/api/games/9999/image")
  assert response.status_code == 404
