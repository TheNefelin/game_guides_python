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


async def test_mark_guide_completed(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  response = await client.post("/api/user-guides/", json={"guide_id": guide["id"]})
  assert response.status_code == 201
  data = response.json()
  assert data["guide_id"] == guide["id"]
  assert data["is_completed"] is True
  assert data["completed_at"] is not None


async def test_mark_guide_completed_upsert(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  first = (await client.post("/api/user-guides/", json={"guide_id": guide["id"]})).json()
  second = await client.post("/api/user-guides/", json={"guide_id": guide["id"]})
  assert second.status_code == 201
  assert second.json()["guide_id"] == first["guide_id"]
  assert second.json()["is_completed"] is True


async def test_mark_guide_unknown_guide(client):
  response = await client.post("/api/user-guides/", json={"guide_id": 9999})
  assert response.status_code == 404
  assert response.json()["detail"] == "Guide not found"


async def test_unmark_guide(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  await client.post("/api/user-guides/", json={"guide_id": guide["id"]})
  response = await client.delete(f"/api/user-guides/{guide['id']}")
  assert response.status_code == 204


async def test_unmark_guide_not_found(client):
  response = await client.delete("/api/user-guides/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "User guide not found"


async def test_unmark_guide_twice(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  await client.delete(f"/api/user-guides/{guide['id']}")
  response = await client.delete(f"/api/user-guides/{guide['id']}")
  assert response.status_code == 404
