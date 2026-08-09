async def _create_game(client, name="Test Game", slug="test-game") -> dict:
  response = await client.post("/api/games/", json={"name": name, "slug": slug})
  return response.json()


async def _create_guide(client, game_id: int, title="Main Story") -> dict:
  response = await client.post("/api/guides/", json={"game_id": game_id, "title": title})
  return response.json()


async def _create_adventure(client, guide_id: int, description="Travel to the past") -> dict:
  response = await client.post("/api/adventures/", json={"guide_id": guide_id, "description": description})
  return response.json()


async def test_user_progress_empty(client):
  game = await _create_game(client)
  response = await client.get(f"/api/user-progress/by-game/{game['id']}")
  assert response.status_code == 200
  data = response.json()
  assert data["guides"] == []
  assert data["adventures"] == []


async def test_user_progress_with_completed_items(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  await client.post("/api/user-guides/", json={"guide_id": guide["id"]})
  await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})

  response = await client.get(f"/api/user-progress/by-game/{game['id']}")
  assert response.status_code == 200
  data = response.json()
  assert len(data["guides"]) == 1
  assert data["guides"][0]["guide_id"] == guide["id"]
  assert data["guides"][0]["is_completed"] is True
  assert len(data["adventures"]) == 1
  assert data["adventures"][0]["adventure_id"] == adventure["id"]
  assert data["adventures"][0]["is_completed"] is True


async def test_user_progress_scoped_to_game(client):
  game1 = await _create_game(client)
  game2 = await _create_game(client, name="Other", slug="other")
  guide1 = await _create_guide(client, game1["id"])
  guide2 = await _create_guide(client, game2["id"], title="Other Guide")
  await client.post("/api/user-guides/", json={"guide_id": guide1["id"]})
  await client.post("/api/user-guides/", json={"guide_id": guide2["id"]})

  response = await client.get(f"/api/user-progress/by-game/{game1['id']}")
  data = response.json()
  assert len(data["guides"]) == 1
  assert data["guides"][0]["guide_id"] == guide1["id"]


async def test_user_progress_reset_by_game(client):
  game = await _create_game(client)
  guide = await _create_guide(client, game["id"])
  adventure = await _create_adventure(client, guide["id"])
  await client.post("/api/user-guides/", json={"guide_id": guide["id"]})
  await client.post("/api/user-adventures/", json={"adventure_id": adventure["id"]})

  response = await client.delete(f"/api/user-progress/by-game/{game['id']}")
  assert response.status_code == 204

  response = await client.get(f"/api/user-progress/by-game/{game['id']}")
  data = response.json()
  assert data["guides"][0]["is_completed"] is False
  assert data["guides"][0]["completed_at"] is None
  assert data["adventures"][0]["is_completed"] is False
  assert data["adventures"][0]["completed_at"] is None
