from collections import deque
import math


def build_adjacency_list(friendships: list[tuple[int, int]]) -> dict[int, set[int]]:
    graph: dict[int, set[int]] = {}

    for user_id_1, user_id_2 in friendships:
        if user_id_1 not in graph:
            graph[user_id_1] = set()
        if user_id_2 not in graph:
            graph[user_id_2] = set()
        graph[user_id_1].add(user_id_2)
        graph[user_id_2].add(user_id_1)

    return graph


def get_mutual_friends(
    user_id: int,
    candidate_id: int,
    graph: dict[int, set[int]]
) -> set[int]:
    user_neighbors = graph.get(user_id, set())
    candidate_neighbors = graph.get(candidate_id, set())
    return user_neighbors & candidate_neighbors


def adamic_adar_score(
    user_id: int,
    candidate_id: int,
    graph: dict[int, set[int]]
) -> float:
    mutual = get_mutual_friends(user_id, candidate_id, graph)
    score = 0.0
    for mutual_friend in mutual:
        degree = len(graph.get(mutual_friend, set()))
        if degree > 1:
            score += 1 / math.log(degree)
    return score


def multi_signal_score(
    user_id: int,
    candidate_id: int,
    graph: dict[int, set[int]],
    distance: int
) -> float:
    return multi_signal_breakdown(
        user_id, candidate_id, graph, distance
    )["final_score"]


def multi_signal_breakdown(
    user_id: int,
    candidate_id: int,
    graph: dict[int, set[int]],
    distance: int
) -> dict[str, float]:
    mutual = get_mutual_friends(user_id, candidate_id, graph)
    mutual_count = len(mutual)

    max_possible = len(graph.get(user_id, set()))
    mutual_score = mutual_count / max_possible if max_possible > 0 else 0.0

    aa_score = adamic_adar_score(user_id, candidate_id, graph)
    aa_normalized = aa_score / (1 + aa_score)

    distance_score = 1.0 / distance if distance > 0 else 0.0

    mutual_component = mutual_score * 0.40
    adamic_adar_component = aa_normalized * 0.40
    distance_component = distance_score * 0.20
    final_score = mutual_component + adamic_adar_component + distance_component

    return {
        "mutual_ratio": round(mutual_score, 4),
        "adamic_adar": round(aa_score, 4),
        "adamic_adar_normalized": round(aa_normalized, 4),
        "distance_score": round(distance_score, 4),
        "mutual_component": round(mutual_component, 4),
        "adamic_adar_component": round(adamic_adar_component, 4),
        "distance_component": round(distance_component, 4),
        "final_score": round(final_score, 4),
    }


def get_recommendations(
    user_id: int,
    graph: dict[int, set[int]],
    limit: int = 10,
    use_multi_signal: bool = True
) -> list[dict]:
    if user_id not in graph:
        return []

    direct_friends = graph[user_id]
    mutual_friends_map: dict[int, set[int]] = {}

    for friend_id in direct_friends:
        for candidate_id in graph.get(friend_id, set()):
            if candidate_id == user_id:
                continue
            if candidate_id in direct_friends:
                continue
            if candidate_id not in mutual_friends_map:
                mutual_friends_map[candidate_id] = set()
            mutual_friends_map[candidate_id].add(friend_id)

    if not mutual_friends_map:
        return []

    distances = bfs_distances(user_id, graph)

    recommendations = []
    for candidate_id, mutual_friends in mutual_friends_map.items():
        distance = distances.get(candidate_id, 999)
        mutual_count = len(mutual_friends)

        if use_multi_signal:
            breakdown = multi_signal_breakdown(user_id, candidate_id, graph, distance)
            score = breakdown["final_score"]
        else:
            score = float(mutual_count)
            breakdown = {
                "mutual_count": float(mutual_count),
                "final_score": score,
            }

        recommendations.append({
            "candidate_id": candidate_id,
            "mutual_friend_count": mutual_count,
            "mutual_friends": list(mutual_friends),
            "score": score,
            "distance": distance
        })
        recommendations[-1]["signals"] = breakdown

    recommendations.sort(
        key=lambda x: (-x["score"], x["candidate_id"])
    )

    return recommendations[:limit]


def bfs_distances(
    start_user_id: int,
    graph: dict[int, set[int]]
) -> dict[int, int]:
    if start_user_id not in graph:
        return {}

    distances: dict[int, int] = {start_user_id: 0}
    queue = deque([start_user_id])

    while queue:
        current_user = queue.popleft()
        current_distance = distances[current_user]

        for neighbor_id in graph.get(current_user, set()):
            if neighbor_id not in distances:
                distances[neighbor_id] = current_distance + 1
                queue.append(neighbor_id)

    return distances


def bfs_path(
    start_user_id: int,
    end_user_id: int,
    graph: dict[int, set[int]]
) -> list[int] | None:
    if start_user_id not in graph or end_user_id not in graph:
        return None

    if start_user_id == end_user_id:
        return [start_user_id]

    visited = {start_user_id}
    queue = deque([[start_user_id]])

    while queue:
        path = queue.popleft()
        current_user = path[-1]

        for neighbor_id in graph.get(current_user, set()):
            if neighbor_id == end_user_id:
                return path + [neighbor_id]

            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append(path + [neighbor_id])

    return None


def get_network_degrees(
    user_id: int,
    graph: dict[int, set[int]]
) -> dict[str, int]:
    if user_id not in graph:
        return {"first": 0, "second": 0, "third": 0}

    distances = bfs_distances(user_id, graph)

    first = sum(1 for d in distances.values() if d == 1)
    second = sum(1 for d in distances.values() if d == 2)
    third = sum(1 for d in distances.values() if d == 3)

    return {"first": first, "second": second, "third": third}
