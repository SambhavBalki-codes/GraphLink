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


def test_typed_response_contracts(client):
    alice = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"},
    ).json()
    bob = client.post(
        "/users",
        json={"name": "Bob", "email": "bob@example.com"},
    ).json()
    charlie = client.post(
        "/users",
        json={"name": "Charlie", "email": "charlie@example.com"},
    ).json()

    client.post("/friendships", json={
        "user_id_1": alice["id"],
        "user_id_2": bob["id"],
    })
    client.post("/friendships", json={
        "user_id_1": bob["id"],
        "user_id_2": charlie["id"],
    })

    recommendation = client.get(f"/users/{alice['id']}/recommendations").json()
    path = client.get(f"/users/{alice['id']}/path/{charlie['id']}").json()
    degrees = client.get(f"/users/{alice['id']}/network").json()
    cache_stats = client.get("/cache/stats").json()
    health = client.get("/health").json()

    assert recommendation["algorithm"] == "v2"
    assert {"user_id", "name", "mutual_friend_count", "mutual_friends", "reason"} <= set(
        recommendation["recommendations"][0]
    ) if recommendation["recommendations"] else True
    assert path["connected"] is True
    assert path["degrees"] == 2
    assert path["path"][0]["user_id"] == alice["id"]
    assert {"user_id", "first_degree", "second_degree", "third_degree"} <= set(degrees)
    assert {"hits", "misses", "hit_rate_percent", "graph_snapshot"} <= set(cache_stats)
    assert {"loaded", "build_count", "nodes"} <= set(cache_stats["graph_snapshot"])
    assert health == {"status": "ok", "database": "healthy"}


def test_openapi_documents_response_models(client):
    schema = client.get("/openapi.json").json()

    assert schema["paths"]["/users/{user_id}/recommendations"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]["$ref"].endswith("/RecommendationResponse")
    assert schema["paths"]["/users/{user_id}/path/{other_user_id}"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]["$ref"].endswith("/ConnectionPathResponse")
    assert schema["paths"]["/cache/stats"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"].endswith("/CacheStatsResponse")


def test_metrics_capture_recommendation_latency_and_cache_hits(client):
    alice = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"},
    ).json()
    bob = client.post(
        "/users",
        json={"name": "Bob", "email": "bob@example.com"},
    ).json()
    client.post("/friendships", json={
        "user_id_1": alice["id"],
        "user_id_2": bob["id"],
    })

    client.get(f"/users/{alice['id']}/recommendations")
    client.get(f"/users/{alice['id']}/recommendations")
    response = client.get("/metrics")

    assert response.status_code == 200
    data = response.json()
    assert data["recommendations"]["count"] == 2
    assert data["recommendations"]["cache_hits"] == 1
    assert data["recommendations"]["average_ms"] >= 0
    assert any(item["path"].endswith("/recommendations") for item in data["requests"])


def test_recommendations_reuse_graph_snapshot_and_cache(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    u3 = client.post("/users", json={"name": "Charlie", "email": "charlie@example.com"}).json()
    u4 = client.post("/users", json={"name": "David", "email": "david@example.com"}).json()

    for left, right in [(u1["id"], u2["id"]), (u1["id"], u3["id"]),
                        (u2["id"], u4["id"]), (u3["id"], u4["id"])]:
        client.post("/friendships", json={"user_id_1": left, "user_id_2": right})

    first = client.get(f"/users/{u1['id']}/recommendations")
    first_stats = client.get("/cache/stats").json()
    second = client.get(f"/users/{u1['id']}/recommendations")
    second_stats = client.get("/cache/stats").json()

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first_stats["graph_snapshot"]["loaded"] is True
    assert second_stats["graph_snapshot"]["build_count"] == first_stats["graph_snapshot"]["build_count"]
    assert second_stats["hits"] == first_stats["hits"] + 1


def test_friendship_changes_invalidate_graph_and_recommendations(client):
    u1 = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
    u2 = client.post("/users", json={"name": "Bob", "email": "bob@example.com"}).json()
    u3 = client.post("/users", json={"name": "Charlie", "email": "charlie@example.com"}).json()

    client.post("/friendships", json={"user_id_1": u1["id"], "user_id_2": u2["id"]})
    client.get(f"/users/{u1['id']}/recommendations")
    loaded_stats = client.get("/cache/stats").json()
    assert loaded_stats["graph_snapshot"]["loaded"] is True
    assert loaded_stats["cached_users"] == 1

    client.post("/friendships", json={"user_id_1": u2["id"], "user_id_2": u3["id"]})
    invalidated_stats = client.get("/cache/stats").json()
    assert invalidated_stats["graph_snapshot"]["loaded"] is False
    assert invalidated_stats["cached_users"] == 0