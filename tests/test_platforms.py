def test_create_platform(client):
  response = client.post("/api/platforms/", json={"name": "PS5"})
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == "PS5"
  assert "id" in data


def test_create_platform_duplicate(client):
  client.post("/api/platforms/", json={"name": "Xbox"})
  response = client.post("/api/platforms/", json={"name": "Xbox"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


def test_get_all_platforms_empty(client):
  response = client.get("/api/platforms/")
  assert response.status_code == 200
  data = response.json()
  assert data["items"] == []
  assert data["total"] == 0
  assert data["page"] == 1
  assert data["limit"] == 20


def test_get_all_platforms(client):
  client.post("/api/platforms/", json={"name": "Switch"})
  client.post("/api/platforms/", json={"name": "PC"})
  response = client.get("/api/platforms/")
  assert response.status_code == 200
  data = response.json()
  assert data["total"] == 2
  # Ordered by name: PC, Switch
  assert data["items"][0]["name"] == "PC"
  assert data["items"][1]["name"] == "Switch"


def test_get_platform_by_id(client):
  created = client.post("/api/platforms/", json={"name": "PS4"}).json()
  response = client.get(f"/api/platforms/{created['id']}")
  assert response.status_code == 200
  assert response.json()["name"] == "PS4"


def test_get_platform_by_id_not_found(client):
  response = client.get("/api/platforms/9999")
  assert response.status_code == 404
  assert response.json()["detail"] == "Platform not found"


def test_update_platform(client):
  created = client.post("/api/platforms/", json={"name": "PS3"}).json()
  response = client.put(f"/api/platforms/{created['id']}", json={"name": "PS3 Pro"})
  assert response.status_code == 200
  assert response.json()["name"] == "PS3 Pro"


def test_update_platform_not_found(client):
  response = client.put("/api/platforms/9999", json={"name": "Nope"})
  assert response.status_code == 404


def test_update_platform_duplicate(client):
  client.post("/api/platforms/", json={"name": "Wii"})
  created = client.post("/api/platforms/", json={"name": "Wii U"}).json()
  response = client.put(f"/api/platforms/{created['id']}", json={"name": "Wii"})
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]


def test_delete_platform(client):
  created = client.post("/api/platforms/", json={"name": "Dreamcast"}).json()
  response = client.delete(f"/api/platforms/{created['id']}")
  assert response.status_code == 204


def test_delete_platform_not_found(client):
  response = client.delete("/api/platforms/9999")
  assert response.status_code == 404


def test_pagination(client):
  for i in range(5):
    client.post("/api/platforms/", json={"name": f"Platform_{i}"})

  response = client.get("/api/platforms/?page=1&limit=2")
  assert response.status_code == 200
  data = response.json()
  assert len(data["items"]) == 2
  assert data["total"] == 5
  assert data["page"] == 1
  assert data["limit"] == 2

  page2 = client.get("/api/platforms/?page=3&limit=2").json()
  assert len(page2["items"]) == 1  # 5th item on page 3
