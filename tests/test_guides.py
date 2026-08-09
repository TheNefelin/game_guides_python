async def _create_game(client) -> dict:
  response = await client.post("/api/games/", json={
    "name": "Test Game",
    "slug": "test-game",
  })
  return response.json()


async def _create_guide(client, game_id: int, **overrides) -> dict:
  payload = {"game_id": game_id, "title": "Main Story", "summary": "The main path"}
  payload.update(overrides)
  response = await client.post("/api/guides/", json=payload)
  return response.json()


async def test_create_guide(client):
  game = await _create_game(client)
  response = await client.post("/api/guides/", json={
    "game_id": game["id"],
    "title": "Main Story",
    "summary": "The main path",
  })
  assert response.status_code == 201
  data = response.json()
  assert data["title"] == "Main Story"
  assert data["game_id"] == game["id"]
  assert data["is_enabled"] is True
  assert "id" in data


async def test_create_guide_unknown_game(client):
  response = await client.post("/api/guides/", json={"game_id": 9999, "title": "Nope"})
  assert response.status_code == 400
  assert "does not exist" in response.json()["detail"]


async def test_get_all_guides_empty(client):
  response = await client.get("/api/guides/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0


async def test_get_all_guides(client):
  game = await _create_game(client)
  await _create_guide(client, game["id"])
  await _create_guide(client, game["id"], title="Side Quests")
  response = await client.get("/api/guides/")
  assert response.status_code == 200
  assert response.json()["total"] == 2


async def test_get_guides_filter_by_game(client):
  game1 = await _create_game(client)
  game2 = (await client.post("/api/games/", json={"name": "Other", "slug": "other"})).json()
  await _create_guide(client, game1["id"])
  await _create_guide(client, game2["id"], title="Other Guide")
  response = await client.get(f"/api/guides/?game_id={game1['id']}")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 1
  assert data["items"][0]["title"] == "Main Story"


async def test_get_guide_by_id(client):
  game = await _create_game(client)
  created = await _create_guide(client, game["id"])
  response = await client.get(f"/api/guides/{created['id']}")
  assert response.status_code == 200
  assert response.json()["title"] == "Main Story"


async def test_get_guide_by_id_not_found(client):
  response = await client.get("/api/guides/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Guide not found"


async def test_get_guides_detail(client):
  game = await _create_game(client)
  await _create_guide(client, game["id"])
  response = await client.get("/api/guides/detail")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 1
  assert data["items"][0]["adventures"] == []


async def test_update_guide(client):
  game = await _create_game(client)
  created = await _create_guide(client, game["id"])
  response = await client.put(f"/api/guides/{created['id']}", json={
    "game_id": game["id"],
    "title": "Main Story Updated",
  })
  assert response.status_code == 200
  assert response.json()["title"] == "Main Story Updated"


async def test_update_guide_not_found(client):
  game = await _create_game(client)
  response = await client.put("/api/guides/9999", json={"game_id": game["id"], "title": "Nope"})
  assert response.status_code == 404


async def test_delete_guide(client):
  game = await _create_game(client)
  created = await _create_guide(client, game["id"])
  response = await client.delete(f"/api/guides/{created['id']}")
  assert response.status_code == 204


async def test_delete_guide_not_found(client):
  response = await client.delete("/api/guides/9999")
  assert response.status_code == 404
