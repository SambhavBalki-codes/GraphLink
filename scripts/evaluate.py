import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from app.database import SessionLocal
from app.models import Friendship
from app.graph import build_adjacency_list, get_recommendations


def evaluate_precision_at_k(k: int = 10, test_users: int = 100, hide_ratio: float = 0.2):
    db = SessionLocal()

    try:
        print(f"Loading friendships from database...")
        all_friendships = db.query(Friendship).all()
        all_pairs = [(f.user_id_1, f.user_id_2) for f in all_friendships]
        print(f"Loaded {len(all_pairs)} friendships")

        full_graph = build_adjacency_list(all_pairs)
        eligible_users = [uid for uid, neighbors in full_graph.items() if len(neighbors) >= 5]
        sample_users = random.sample(eligible_users, min(test_users, len(eligible_users)))

        print(f"Evaluating {len(sample_users)} users...")

        v1_precisions = []
        v2_precisions = []

        for user_id in sample_users:
            neighbors = list(full_graph[user_id])
            hide_count = max(1, int(len(neighbors) * hide_ratio))
            hidden_friends = set(random.sample(neighbors, hide_count))

            test_pairs = [
                (a, b) for a, b in all_pairs
                if not (
                    (a == user_id and b in hidden_friends) or
                    (b == user_id and a in hidden_friends)
                )
            ]

            test_graph = build_adjacency_list(test_pairs)

            v1_recs = get_recommendations(user_id, test_graph, k, use_multi_signal=False)
            v2_recs = get_recommendations(user_id, test_graph, k, use_multi_signal=True)

            v1_candidates = {r["candidate_id"] for r in v1_recs}
            v2_candidates = {r["candidate_id"] for r in v2_recs}

            v1_hits = len(hidden_friends & v1_candidates)
            v2_hits = len(hidden_friends & v2_candidates)

            v1_precisions.append(v1_hits / k)
            v2_precisions.append(v2_hits / k)

        avg_v1 = sum(v1_precisions) / len(v1_precisions)
        avg_v2 = sum(v2_precisions) / len(v2_precisions)

        print(f"\n{'='*50}")
        print(f"Precision@{k} Evaluation Results")
        print(f"{'='*50}")
        print(f"Test users:        {len(sample_users)}")
        print(f"Hidden ratio:      {hide_ratio * 100}%")
        print(f"K:                 {k}")
        print(f"")
        print(f"V1 (mutual friends only): {avg_v1:.4f} ({avg_v1*100:.2f}%)")
        print(f"V2 (multi-signal):        {avg_v2:.4f} ({avg_v2*100:.2f}%)")
        print(f"")
        improvement = ((avg_v2 - avg_v1) / avg_v1 * 100) if avg_v1 > 0 else 0
        print(f"V2 improvement over V1: {improvement:.1f}%")
        print(f"{'='*50}")

    finally:
        db.close()


if __name__ == "__main__":
    random.seed(42)
    evaluate_precision_at_k(k=10, test_users=100, hide_ratio=0.2)