async def _create_game(client) -> dict:
  response = await client.post("/api/games/", json={
    "name": "Test Game",
    "slug": "test-game",
    "description": "A game for testing",
  })
  return response.json()


async def test_create_source(client):
  game = await _create_game(client)
  response = await client.post("/api/sources/", json={
    "game_id": game["id"],
    "name": "Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Game",
  })
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == "Wikipedia"
  assert data["url"] == "https://en.wikipedia.org/wiki/Game"
  assert data["game_id"] == game["id"]
  assert "id" in data


async def test_create_source_duplicate_name(client):
  game = await _create_game(client)
  await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://wiki.com"})
  response = await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://other.com"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_get_all_sources_empty(client):
  response = await client.get("/api/sources/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0


async def test_get_all_sources(client):
  game = await _create_game(client)
  await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://wiki.com"})
  await client.post("/api/sources/", json={"game_id": game["id"], "name": "Guide", "url": "https://guide.com"})
  response = await client.get("/api/sources/")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 2


async def test_get_sources_filter_by_game(client):
  game1 = await _create_game(client)
  game2 = (await client.post("/api/games/", json={"name": "Other", "slug": "other"})).json()
  await client.post("/api/sources/", json={"game_id": game1["id"], "name": "Wiki", "url": "https://wiki.com"})
  await client.post("/api/sources/", json={"game_id": game2["id"], "name": "Other", "url": "https://other.com"})
  response = await client.get(f"/api/sources/?game_id={game1['id']}")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 1
  assert data["items"][0]["name"] == "Wiki"


async def test_get_source_by_id(client):
  game = await _create_game(client)
  created = (await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://wiki.com"})).json()
  response = await client.get(f"/api/sources/{created['id']}")
  assert response.status_code == 200
  assert response.json()["name"] == "Wiki"


async def test_get_source_by_id_not_found(client):
  response = await client.get("/api/sources/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Source not found"


async def test_update_source(client):
  game = await _create_game(client)
  created = (await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://wiki.com"})).json()
  response = await client.put(f"/api/sources/{created['id']}", json={"game_id": game["id"], "name": "Guide", "url": "https://guide.com"})
  assert response.status_code == 200
  assert response.json()["name"] == "Guide"
  assert response.json()["url"] == "https://guide.com"


async def test_update_source_not_found(client):
  game = await _create_game(client)
  response = await client.put("/api/sources/9999", json={"game_id": game["id"], "name": "Nope", "url": "https://nope.com"})
  assert response.status_code == 404


async def test_update_source_duplicate(client):
  game = await _create_game(client)
  await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://wiki.com"})
  created = (await client.post("/api/sources/", json={"game_id": game["id"], "name": "Other", "url": "https://other.com"})).json()
  response = await client.put(f"/api/sources/{created['id']}", json={"game_id": game["id"], "name": "Wiki", "url": "https://other.com"})
  assert response.status_code == 400


async def test_delete_source(client):
  game = await _create_game(client)
  created = (await client.post("/api/sources/", json={"game_id": game["id"], "name": "Wiki", "url": "https://wiki.com"})).json()
  response = await client.delete(f"/api/sources/{created['id']}")
  assert response.status_code == 204


async def test_delete_source_not_found(client):
  response = await client.delete("/api/sources/9999")
  assert response.status_code == 404
