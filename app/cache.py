import time
from collections import OrderedDict
from collections.abc import Callable
from threading import Lock


class RecommendationCache:
    def __init__(self, max_size: int = 100, ttl_seconds: float = 300):
        self._cache = OrderedDict()
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._lock = Lock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
        self._invalidations = 0

    def get(self, key):
        now = time.monotonic()
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None
            if entry["expires_at"] <= now:
                del self._cache[key]
                self._expirations += 1
                self._misses += 1
                return None
            self._cache.move_to_end(key)
            self._hits += 1
            return entry["data"]

    def set(self, key, data: dict):
        with self._lock:
            self._cache[key] = {
                "data": data,
                "expires_at": time.monotonic() + self._ttl_seconds,
            }
            self._cache.move_to_end(key)
            while len(self._cache) > self._max_size:
                self._cache.popitem(last=False)
                self._evictions += 1

    def invalidate(self, key):
        with self._lock:
            if self._cache.pop(key, None) is not None:
                self._invalidations += 1

    def invalidate_user_and_friends(self, user_id: int, friend_ids: list[int]):
        user_ids = {user_id, *friend_ids}
        with self._lock:
            keys = [key for key in self._cache if key[0] in user_ids]
            for key in keys:
                del self._cache[key]
            self._invalidations += len(keys)

    def clear(self):
        with self._lock:
            self._cache.clear()

    def invalidate_all(self):
        with self._lock:
            self._invalidations += len(self._cache)
            self._cache.clear()

    def stats(self):
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0
            return {
                "cached_entries": len(self._cache),
                "cached_users": len(self._cache),
                "max_size": self._max_size,
                "ttl_seconds": self._ttl_seconds,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate_percent": round(hit_rate, 2),
                "evictions": self._evictions,
                "expirations": self._expirations,
                "invalidations": self._invalidations,
            }


recommendation_cache = RecommendationCache(max_size=100, ttl_seconds=300)


class GraphSnapshotCache:
    def __init__(self):
        self._graph = None
        self._lock = Lock()
        self._build_count = 0
        self._last_build_seconds = 0.0
        self._total_build_seconds = 0.0

    def get_or_build(self, builder: Callable):
        with self._lock:
            if self._graph is None:
                started = time.perf_counter()
                self._graph = builder()
                elapsed = time.perf_counter() - started
                self._last_build_seconds = elapsed
                self._total_build_seconds += elapsed
                self._build_count += 1
            return self._graph

    def invalidate(self):
        with self._lock:
            self._graph = None

    def stats(self):
        with self._lock:
            return {
                "loaded": self._graph is not None,
                "build_count": self._build_count,
                "nodes": len(self._graph) if self._graph is not None else 0,
                "last_build_ms": round(self._last_build_seconds * 1000, 3),
                "total_build_ms": round(self._total_build_seconds * 1000, 3),
            }


graph_snapshot_cache = GraphSnapshotCache()
