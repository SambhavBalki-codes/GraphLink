from collections import deque


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


def get_recommendations(
    user_id: int,
    graph: dict[int, set[int]],
    limit: int = 10
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

    recommendations = []
    for candidate_id, mutual_friends in mutual_friends_map.items():
        recommendations.append({
            "candidate_id": candidate_id,
            "mutual_friend_count": len(mutual_friends),
            "mutual_friends": list(mutual_friends)
        })

    recommendations.sort(
        key=lambda x: (-x["mutual_friend_count"], x["candidate_id"])
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
