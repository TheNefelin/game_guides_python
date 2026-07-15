async def test_create_platform(client):
  response = await client.post("/api/platforms/", json={"name": "PS5"})
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == "PS5"
  assert "id" in data


async def test_create_platform_duplicate(client):
  await client.post("/api/platforms/", json={"name": "Xbox"})
  response = await client.post("/api/platforms/", json={"name": "Xbox"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_get_all_platforms_empty(client):
  response = await client.get("/api/platforms/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0
  assert data["page"] == 1
  assert data["limit"] == 20


async def test_get_all_platforms(client):
  await client.post("/api/platforms/", json={"name": "Switch"})
  await client.post("/api/platforms/", json={"name": "PC"})
  response = await client.get("/api/platforms/")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 2
  # Ordered by name: PC, Switch
  assert data["items"][0]["name"] == "PC"
  assert data["items"][1]["name"] == "Switch"


async def test_get_platform_by_id(client):
  created = (await client.post("/api/platforms/", json={"name": "PS4"})).json()
  response = await client.get(f"/api/platforms/{created['id']}")
  assert response.status_code == 200
  assert response.json()["name"] == "PS4"


async def test_get_platform_by_id_not_found(client):
  response = await client.get("/api/platforms/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Platform not found"


async def test_update_platform(client):
  created = (await client.post("/api/platforms/", json={"name": "PS3"})).json()
  response = await client.put(f"/api/platforms/{created['id']}", json={"name": "PS3 Pro"})
  assert response.status_code == 200
  assert response.json()["name"] == "PS3 Pro"


async def test_update_platform_not_found(client):
  response = await client.put("/api/platforms/9999", json={"name": "Nope"})
  assert response.status_code == 404


async def test_update_platform_duplicate(client):
  await client.post("/api/platforms/", json={"name": "Wii"})
  created = (await client.post("/api/platforms/", json={"name": "Wii U"})).json()
  response = await client.put(f"/api/platforms/{created['id']}", json={"name": "Wii"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


async def test_delete_platform(client):
  created = (await client.post("/api/platforms/", json={"name": "Dreamcast"})).json()
  response = await client.delete(f"/api/platforms/{created['id']}")
  assert response.status_code == 204


async def test_delete_platform_not_found(client):
  response = await client.delete("/api/platforms/9999")
  assert response.status_code == 404


async def test_pagination(client):
  for i in range(5):
    await client.post("/api/platforms/", json={"name": f"Platform_{i}"})

  response = await client.get("/api/platforms/?page=1&limit=2")
  assert response.status_code == 200
  data = response.json()
  assert len(data["items"]) == 2
  assert data["total"] == 5
  assert data["page"] == 1
  assert data["limit"] == 2

  page2 = (await client.get("/api/platforms/?page=3&limit=2")).json()
  assert len(page2["items"]) == 1  # 5th item on page 3
