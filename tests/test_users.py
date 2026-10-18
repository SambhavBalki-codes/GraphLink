def test_create_user(client):
    response = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_create_duplicate_email(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    response = client.post("/users", json={"name": "Alice2", "email": "alice@example.com"})
    assert response.status_code == 409


def test_get_user(client):
    created = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    user_id = created.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_nonexistent_user(client):
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_list_users(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_user(client):
    created = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    user_id = created.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_invalid_email(client):
    response = client.post("/users", json={"name": "Alice", "email": "notanemail"})
    assert response.status_code == 422