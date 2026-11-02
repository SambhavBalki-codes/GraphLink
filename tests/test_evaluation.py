import math

from scripts.evaluate import _metric_values, _write_output, evaluate_graph


def test_metric_values_use_standard_precision_recall_and_ndcg():
    metrics = _metric_values(
        [{"candidate_id": 10}, {"candidate_id": 20}, {"candidate_id": 30}],
        {10, 40},
        k=3,
    )

    expected_ndcg = 1 / (1 + 1 / math.log2(3))
    assert metrics["precision"] == 1 / 3
    assert metrics["recall"] == 1 / 2
    assert math.isclose(metrics["ndcg"], expected_ndcg)


def test_evaluation_is_reproducible_with_fixed_seeds():
    pairs = [
        (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
        (2, 3), (2, 4), (2, 5),
        (3, 4), (3, 5),
        (4, 5), (4, 6),
        (5, 6),
    ]

    first = evaluate_graph(
        pairs,
        k=3,
        test_users=4,
        hide_ratio=0.2,
        runs=3,
        split_seed=7,
        evaluation_seed=11,
    )
    second = evaluate_graph(
        pairs,
        k=3,
        test_users=4,
        hide_ratio=0.2,
        runs=3,
        split_seed=7,
        evaluation_seed=11,
    )

    assert first == second
    assert first["configuration"]["test_users_evaluated"] == 3
    assert set(first["summary"]) == {"v1", "v2"}
    assert set(first["summary"]["v2"]) == {"precision", "recall", "ndcg"}
    assert "improvement_percent" in first["summary"]["v2"]["precision"]


def test_evaluation_writes_json_and_csv(tmp_path):
    report = evaluate_graph(
        [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4)],
        k=2,
        test_users=2,
        runs=1,
    )
    json_path = tmp_path / "evaluation.json"
    csv_path = tmp_path / "evaluation.csv"

    _write_output(report, json_path)
    _write_output(report, csv_path)

    assert '"summary"' in json_path.read_text(encoding="utf-8")
    assert "run,algorithm,precision,recall,ndcg" in csv_path.read_text(encoding="utf-8")
