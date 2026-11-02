from collections import defaultdict, deque
from threading import Lock
import time


class Metrics:
    def __init__(self, max_samples: int = 1000):
        self._lock = Lock()
        self._requests = defaultdict(lambda: {"count": 0, "errors": 0, "total_ms": 0.0})
        self._recommendations = {"count": 0, "total_ms": 0.0, "cache_hits": 0}
        self._recent_latencies = deque(maxlen=max_samples)

    def record_request(self, method: str, path: str, status_code: int, duration_ms: float):
        with self._lock:
            item = self._requests[(method, path)]
            item["count"] += 1
            item["total_ms"] += duration_ms
            if status_code >= 400:
                item["errors"] += 1
            self._recent_latencies.append(duration_ms)

    def record_recommendation(self, duration_ms: float, cache_hit: bool):
        with self._lock:
            self._recommendations["count"] += 1
            self._recommendations["total_ms"] += duration_ms
            if cache_hit:
                self._recommendations["cache_hits"] += 1

    def reset(self):
        with self._lock:
            self._requests.clear()
            self._recommendations = {"count": 0, "total_ms": 0.0, "cache_hits": 0}
            self._recent_latencies.clear()

    def snapshot(self):
        with self._lock:
            endpoints = []
            for (method, path), item in sorted(self._requests.items()):
                endpoints.append({
                    "method": method,
                    "path": path,
                    "requests": item["count"],
                    "errors": item["errors"],
                    "average_ms": round(item["total_ms"] / item["count"], 3),
                })
            count = self._recommendations["count"]
            return {
                "requests": endpoints,
                "recommendations": {
                    "count": count,
                    "average_ms": round(
                        self._recommendations["total_ms"] / count, 3
                    ) if count else 0.0,
                    "cache_hits": self._recommendations["cache_hits"],
                },
                "recent_average_ms": round(
                    sum(self._recent_latencies) / len(self._recent_latencies), 3
                ) if self._recent_latencies else 0.0,
            }


metrics = Metrics()
