import argparse
import csv
import json
import math
import os
import random
import sys
from pathlib import Path
from statistics import mean, stdev

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.graph import build_adjacency_list, get_recommendations
from app.models import Friendship


def _metric_values(recommendations, relevant_ids: set[int], k: int):
    recommended_ids = [item["candidate_id"] for item in recommendations[:k]]
    hits = [int(candidate_id in relevant_ids) for candidate_id in recommended_ids]
    hit_count = sum(hits)

    precision = hit_count / k
    recall = hit_count / len(relevant_ids) if relevant_ids else 0.0

    dcg = sum(
        relevance / math.log2(rank + 2)
        for rank, relevance in enumerate(hits)
    )
    ideal_hits = min(len(relevant_ids), k)
    ideal_dcg = sum(
        1 / math.log2(rank + 2)
        for rank in range(ideal_hits)
    )
    ndcg = dcg / ideal_dcg if ideal_dcg else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "ndcg": ndcg,
        "recommendations": len(recommended_ids),
    }


def _evaluate_user(
    user_id: int,
    full_graph: dict[int, set[int]],
    all_pairs: list[tuple[int, int]],
    hide_ratio: float,
    k: int,
    rng: random.Random,
):
    neighbors = sorted(full_graph[user_id])
    hide_count = max(1, int(len(neighbors) * hide_ratio))
    hidden_friends = set(rng.sample(neighbors, hide_count))
    hidden_edges = {
        tuple(sorted((user_id, friend_id))) for friend_id in hidden_friends
    }
    test_pairs = [pair for pair in all_pairs if tuple(pair) not in hidden_edges]
    test_graph = build_adjacency_list(test_pairs)

    results = {}
    for algorithm, use_multi_signal in (("v1", False), ("v2", True)):
        recommendations = get_recommendations(
            user_id,
            test_graph,
            k,
            use_multi_signal=use_multi_signal,
        )
        results[algorithm] = _metric_values(recommendations, hidden_friends, k)
    return results


def _summarize(runs: list[dict], algorithm: str):
    metrics = {}
    for metric in ("precision", "recall", "ndcg"):
        values = [run[algorithm][metric] for run in runs]
        metrics[metric] = {
            "mean": mean(values),
            "stddev": stdev(values) if len(values) > 1 else 0.0,
        }
    return metrics


def evaluate_graph(
    all_pairs: list[tuple[int, int]],
    k: int = 10,
    test_users: int = 100,
    hide_ratio: float = 0.2,
    runs: int = 5,
    split_seed: int = 42,
    evaluation_seed: int = 1000,
):
    if not 0 < hide_ratio <= 1:
        raise ValueError("hide_ratio must be greater than 0 and at most 1")
    if k < 1 or test_users < 1 or runs < 1:
        raise ValueError("k, test_users, and runs must be positive")

    full_graph = build_adjacency_list(all_pairs)
    eligible_users = sorted(
        user_id for user_id, neighbors in full_graph.items() if len(neighbors) >= 5
    )
    split_rng = random.Random(split_seed)
    sample_users = split_rng.sample(
        eligible_users,
        min(test_users, len(eligible_users)),
    )

    run_results = []
    for run_index in range(runs):
        rng = random.Random(evaluation_seed + run_index)
        user_results = {algorithm: [] for algorithm in ("v1", "v2")}
        for user_id in sample_users:
            result = _evaluate_user(
                user_id,
                full_graph,
                all_pairs,
                hide_ratio,
                k,
                rng,
            )
            for algorithm in user_results:
                user_results[algorithm].append(result[algorithm])

        run_results.append({
            algorithm: {
                metric: mean(values[metric] for values in user_results[algorithm])
                for metric in ("precision", "recall", "ndcg")
            }
            for algorithm in user_results
        })

    summary = {
        algorithm: _summarize(run_results, algorithm)
        for algorithm in ("v1", "v2")
    }
    v1_precision = summary["v1"]["precision"]["mean"]
    v2_precision = summary["v2"]["precision"]["mean"]
    summary["v2"]["precision"]["improvement_percent"] = (
        (v2_precision - v1_precision) / v1_precision * 100
        if v1_precision
        else 0.0
    )

    return {
        "configuration": {
            "k": k,
            "test_users_requested": test_users,
            "test_users_evaluated": len(sample_users),
            "hide_ratio": hide_ratio,
            "runs": runs,
            "split_seed": split_seed,
            "evaluation_seed": evaluation_seed,
            "friendships": len(all_pairs),
        },
        "summary": summary,
        "runs": run_results,
    }


def _print_report(report: dict):
    config = report["configuration"]
    print("\n" + "=" * 68)
    print(f"Precision/Recall/NDCG@{config['k']} Evaluation")
    print("=" * 68)
    print(f"Users:       {config['test_users_evaluated']} fixed users")
    print(f"Runs:        {config['runs']}")
    print(f"Hidden ratio:{config['hide_ratio'] * 100:.0f}%")
    print(f"Split seed:  {config['split_seed']}")
    print(f"Eval seed:   {config['evaluation_seed']} (+ run index)")
    print()
    print("Algorithm              Precision       Recall          NDCG")
    for algorithm, label in (("v1", "V1 baseline"), ("v2", "V2 multi-signal")):
        values = report["summary"][algorithm]
        print(
            f"{label:<21}"
            f"{values['precision']['mean']:.4f} ± {values['precision']['stddev']:.4f}  "
            f"{values['recall']['mean']:.4f} ± {values['recall']['stddev']:.4f}  "
            f"{values['ndcg']['mean']:.4f} ± {values['ndcg']['stddev']:.4f}"
        )
    improvement = report["summary"]["v2"]["precision"]["improvement_percent"]
    print(f"\nV2 Precision@K improvement: {improvement:.2f}%")
    print("=" * 68)


def _write_output(report: dict, output_path: Path):
    if output_path.suffix.lower() == ".csv":
        rows = []
        for run_index, run in enumerate(report["runs"], start=1):
            for algorithm, values in run.items():
                rows.append({
                    "run": run_index,
                    "algorithm": algorithm,
                    **values,
                })
        with output_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    else:
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)


def evaluate_precision_at_k(
    k: int = 10,
    test_users: int = 100,
    hide_ratio: float = 0.2,
    runs: int = 5,
    split_seed: int = 42,
    evaluation_seed: int = 1000,
    output: str | None = None,
):
    db = SessionLocal()
    try:
        all_friendships = db.query(Friendship).all()
        all_pairs = [(friendship.user_id_1, friendship.user_id_2) for friendship in all_friendships]
        report = evaluate_graph(
            all_pairs,
            k=k,
            test_users=test_users,
            hide_ratio=hide_ratio,
            runs=runs,
            split_seed=split_seed,
            evaluation_seed=evaluation_seed,
        )
        _print_report(report)
        if output:
            _write_output(report, Path(output))
        return report
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Evaluate GraphLink recommendations.")
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--test-users", type=int, default=100)
    parser.add_argument("--hide-ratio", type=float, default=0.2)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--split-seed", type=int, default=42)
    parser.add_argument("--evaluation-seed", type=int, default=1000)
    parser.add_argument("--output", help="Write JSON by default, or CSV when ending in .csv.")
    args = parser.parse_args()
    evaluate_precision_at_k(**vars(args))


if __name__ == "__main__":
    main()
