from app.graph import build_adjacency_list, get_recommendations, bfs_distances


def test_build_adjacency_list_basic():
    friendships = [(1, 2), (1, 3)]
    graph = build_adjacency_list(friendships)
    assert graph[1] == {2, 3}
    assert graph[2] == {1}
    assert graph[3] == {1}


def test_build_adjacency_list_undirected():
    friendships = [(1, 2)]
    graph = build_adjacency_list(friendships)
    assert 2 in graph[1]
    assert 1 in graph[2]


def test_empty_friendships():
    graph = build_adjacency_list([])
    assert graph == {}


def test_no_friends_no_recommendations():
    graph = {1: set()}
    result = get_recommendations(1, graph)
    assert result == []


def test_user_not_in_graph():
    graph = {1: {2}, 2: {1}}
    result = get_recommendations(99, graph)
    assert result == []


def test_basic_recommendation():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph)
    assert len(result) == 1
    assert result[0]["candidate_id"] == 4
    assert result[0]["mutual_friend_count"] == 2


def test_direct_friends_excluded():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph)
    candidate_ids = [r["candidate_id"] for r in result]
    assert 2 not in candidate_ids
    assert 3 not in candidate_ids


def test_target_user_excluded():
    friendships = [(1, 2), (2, 3), (1, 3)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph)
    candidate_ids = [r["candidate_id"] for r in result]
    assert 1 not in candidate_ids


def test_ranking_by_mutual_friend_count():
    friendships = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5), (2, 6)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph)
    assert result[0]["candidate_id"] == 5
    assert result[0]["mutual_friend_count"] == 3
    assert result[1]["candidate_id"] == 6
    assert result[1]["mutual_friend_count"] == 1


def test_tie_breaking_by_user_id():
    friendships = [(1, 2), (2, 3), (2, 4)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph)
    assert result[0]["candidate_id"] == 3
    assert result[1]["candidate_id"] == 4


def test_recommendation_limit():
    friendships = [(1, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph, limit=3)
    assert len(result) <= 3


def test_bfs_distances_basic():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    distances = bfs_distances(1, graph)
    assert distances[1] == 0
    assert distances[2] == 1
    assert distances[3] == 1
    assert distances[4] == 2


def test_bfs_disconnected_graph():
    friendships = [(1, 2), (3, 4)]
    graph = build_adjacency_list(friendships)
    distances = bfs_distances(1, graph)
    assert 3 not in distances
    assert 4 not in distances


def test_bfs_user_not_in_graph():
    graph = {1: {2}, 2: {1}}
    distances = bfs_distances(99, graph)
    assert distances == {}