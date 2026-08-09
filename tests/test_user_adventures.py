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


async def test_mark_adventure_completed(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  response = await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})
  assert response.status_code == 201
  data = response.json()
  assert data["adventure_id"] == adventure["id"]
  assert data["is_completed"] is True
  assert data["completed_at"] is not None


async def test_mark_adventure_completed_upsert(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})
  response = await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})
  assert response.status_code == 201
  assert response.json()["is_completed"] is True


async def test_mark_adventure_unknown_adventure(client):
  response = await client.post("/api/user-adventures/", json={"adventure_id": 9999})
  assert response.status_code == 404
  assert response.json()["detail"] == "Adventure not found"


async def test_unmark_adventure(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})
  response = await client.delete(f"/api/user-adventures/{adventure['id']}")
  assert response.status_code == 204


async def test_unmark_adventure_not_found(client):
  response = await client.delete("/api/user-adventures/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "User adventure not found"
