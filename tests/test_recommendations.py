def test_recommendations_basic(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    u3 = client.post("/users", json={"name": "Charlie", "email": "charlie@example.com"}).json()
    u4 = client.post("/users", json={"name": "David", "email": "david@example.com"}).json()

    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u3["id"]})
    client.post("/friendships", json={"user_id_1": u2["id"], "user_id_2": u4["id"]})
    client.post("/friendships", json={"user_id_1": u3["id"], "user_id_2": u4["id"]})

    response = client.get(f"/users/{u1['id']}/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert data["recommendations"][0]["user_id"] == u4["id"]
    assert data["recommendations"][0]["mutual_friend_count"] == 2


def test_no_recommendations_for_isolated_user(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    response = client.get(f"/users/{u1['id']}/recommendations")
    assert response.status_code == 200
    assert response.json()["recommendations"] == []


def test_recommendations_exclude_direct_friends(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    u3 = client.post("/users", json={"name": "Charlie", "email": "charlie@example.com"}).json()

    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    client.post("/friendships", json={"user_id_1": u2["id"], "user_id_2": u3["id"]})
    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u3["id"]})

    response = client.get(f"/users/{u1['id']}/recommendations")
    candidate_ids = [r["user_id"] for r in response.json()["recommendations"]]
    assert u2["id"] not in candidate_ids
    assert u3["id"] not in candidate_ids


def test_recommendations_nonexistent_user(client):
    response = client.get("/users/9999/recommendations")
    assert response.status_code == 404


def test_recommendations_limit(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    for i in range(5):
        u = client.post("/users", json={"name": f"User{i}", "email": f"user{i}@example.com"}).json()
        client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
        client.post("/friendships", json={"user_id_1": u2["id"], "user_id_2": u["id"]})

    response = client.get(f"/users/{u1['id']}/recommendations?limit=2")
    assert len(response.json()["recommendations"]) <= 2


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_network_stats(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["total_users"] == 2