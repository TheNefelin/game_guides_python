async def test_create_genre(client):
  response = await client.post("/api/genres/", json={"name": "RPG"})
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == "RPG"
  assert "id" in data


async def test_create_genre_duplicate(client):
  await client.post("/api/genres/", json={"name": "Action"})
  response = await client.post("/api/genres/", json={"name": "Action"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_get_all_genres_empty(client):
  response = await client.get("/api/genres/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0


async def test_get_all_genres(client):
  await client.post("/api/genres/", json={"name": "Adventure"})
  await client.post("/api/genres/", json={"name": "Puzzle"})
  response = await client.get("/api/genres/")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 2
  # Ordered by name: Adventure, Puzzle
  assert data["items"][0]["name"] == "Adventure"
  assert data["items"][1]["name"] == "Puzzle"


async def test_get_genre_by_id(client):
  created = (await client.post("/api/genres/", json={"name": "JRPG"})).json()
  response = await client.get(f"/api/genres/{created['id']}")
  assert response.status_code == 200
  assert response.json()["name"] == "JRPG"


async def test_get_genre_by_id_not_found(client):
  response = await client.get("/api/genres/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Genre not found"


async def test_update_genre(client):
  created = (await client.post("/api/genres/", json={"name": "FPS"})).json()
  response = await client.put(f"/api/genres/{created['id']}", json={"name": "Shooter"})
  assert response.status_code == 200
  assert response.json()["name"] == "Shooter"


async def test_update_genre_not_found(client):
  response = await client.put("/api/genres/9999", json={"name": "Nope"})
  assert response.status_code == 404


async def test_update_genre_duplicate(client):
  await client.post("/api/genres/", json={"name": "Strategy"})
  created = (await client.post("/api/genres/", json={"name": "Tactical"})).json()
  response = await client.put(f"/api/genres/{created['id']}", json={"name": "Strategy"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_delete_genre(client):
  created = (await client.post("/api/genres/", json={"name": "Simulation"})).json()
  response = await client.delete(f"/api/genres/{created['id']}")
  assert response.status_code == 204


async def test_delete_genre_not_found(client):
  response = await client.delete("/api/genres/9999")
  assert response.status_code == 404


async def test_pagination(client):
  for i in range(5):
    await client.post("/api/genres/", json={"name": f"Genre_{i}"})

  response = await client.get("/api/genres/?page=1&limit=2")
  assert response.status_code == 200
  data = response.json()
  assert len(data["items"]) == 2
  assert data["total"] == 5

  page2 = (await client.get("/api/genres/?page=3&limit=2")).json()
  assert len(page2["items"]) == 1
