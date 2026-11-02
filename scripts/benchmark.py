import os
import random
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.graph import build_adjacency_list, get_recommendations


def generate_synthetic_network(num_users: int, avg_friends: int = 10):
    friendships = set()
    for user_id in range(1, num_users + 1):
        num_friends = random.randint(1, avg_friends * 2)
        for _ in range(num_friends):
            friend_id = random.randint(1, num_users)
            if friend_id != user_id:
                small_id = min(user_id, friend_id)
                large_id = max(user_id, friend_id)
                friendships.add((small_id, large_id))
    return list(friendships)


def run_benchmark(num_users: int, iterations: int = 5):
    print(f"\n{'='*50}")
    print(f"Network size: {num_users} users")
    print(f"{'='*50}")

    friendships = generate_synthetic_network(num_users)
    print(f"Generated {len(friendships)} friendships")

    build_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        graph = build_adjacency_list(friendships)
        end = time.perf_counter()
        build_times.append(end - start)

    avg_build = sum(build_times) / len(build_times)
    print(f"Avg graph build time: {avg_build * 1000:.2f} ms")

    target_user = random.randint(1, num_users)

    rec_times = []
    for _ in range(iterations):
        graph = build_adjacency_list(friendships)
        start = time.perf_counter()
        recommendations = get_recommendations(target_user, graph, limit=10)
        end = time.perf_counter()
        rec_times.append(end - start)

    avg_rec = sum(rec_times) / len(rec_times)
    print(f"Avg recommendation time: {avg_rec * 1000:.2f} ms")
    print(f"Recommendations returned: {len(recommendations)}")
    print(f"Total avg time: {(avg_build + avg_rec) * 1000:.2f} ms")


if __name__ == "__main__":
    random.seed(42)
    print("GraphLink Performance Benchmark")
    print("================================")

    for size in [1000, 5000, 10000]:
        run_benchmark(size)

    print("\nBenchmark complete.")