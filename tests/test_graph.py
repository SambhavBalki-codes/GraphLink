from app.graph import build_adjacency_list, get_recommendations, bfs_distances, adamic_adar_score, multi_signal_score, bfs_path, get_network_degrees

def test_adamic_adar_score_basic():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    from app.graph import adamic_adar_score
    score = adamic_adar_score(1, 4, graph)
    assert score > 0


def test_adamic_adar_no_mutual_friends():
    friendships = [(1, 2), (3, 4)]
    graph = build_adjacency_list(friendships)
    from app.graph import adamic_adar_score
    score = adamic_adar_score(1, 3, graph)
    assert score == 0.0


def test_multi_signal_score_basic():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    from app.graph import multi_signal_score
    score = multi_signal_score(1, 4, graph, distance=2)
    assert 0.0 < score <= 1.0


def test_bfs_path_basic():
    friendships = [(1, 2), (2, 4), (1, 3), (3, 4)]
    graph = build_adjacency_list(friendships)
    from app.graph import bfs_path
    path = bfs_path(1, 4, graph)
    assert path is not None
    assert path[0] == 1
    assert path[-1] == 4
    assert len(path) == 3


def test_bfs_path_no_connection():
    friendships = [(1, 2), (3, 4)]
    graph = build_adjacency_list(friendships)
    from app.graph import bfs_path
    path = bfs_path(1, 3, graph)
    assert path is None


def test_bfs_path_same_user():
    friendships = [(1, 2)]
    graph = build_adjacency_list(friendships)
    from app.graph import bfs_path
    path = bfs_path(1, 1, graph)
    assert path == [1]


def test_get_network_degrees():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6)]
    graph = build_adjacency_list(friendships)
    from app.graph import get_network_degrees
    degrees = get_network_degrees(1, graph)
    assert degrees["first"] == 2
    assert degrees["second"] == 2
    assert degrees["third"] == 1


def test_recommendations_have_score():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    result = get_recommendations(1, graph)
    assert "score" in result[0]
    assert result[0]["score"] > 0


def test_recommendations_v1_vs_v2():
    friendships = [(1, 2), (1, 3), (2, 4), (3, 4)]
    graph = build_adjacency_list(friendships)
    v1 = get_recommendations(1, graph, use_multi_signal=False)
    v2 = get_recommendations(1, graph, use_multi_signal=True)
    assert len(v1) == len(v2)
    assert v1[0]["candidate_id"] == v2[0]["candidate_id"]