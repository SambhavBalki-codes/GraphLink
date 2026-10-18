def test_create_friendship(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    response = client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    assert response.status_code == 201


def test_duplicate_friendship(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    response = client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    assert response.status_code == 409


def test_self_friendship(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    response = client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u1["id"]})
    assert response.status_code == 400


def test_friendship_nonexistent_user(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    response = client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": 9999})
    assert response.status_code == 404


def test_delete_friendship(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    response = client.request("DELETE", "/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    assert response.status_code == 200


def test_get_friends(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    response = client.get(f"/users/{u1['id']}/friends")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Bob"


def test_reversed_friendship_ids(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    response = client.post("/friendships", json={"user_id_1": u2["id"], "user_id_2": u1["id"]})
    assert response.status_code == 409