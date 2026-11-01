from threading import Lock
import time


class RecommendationCache:
    def __init__(self, max_size: int = 100):
        self._cache: dict = {}
        self._access_times: dict = {}
        self._max_size = max_size
        self._lock = Lock()
        self._hits = 0
        self._misses = 0

    def get(self, user_id: int):
        with self._lock:
            if user_id in self._cache:
                self._access_times[user_id] = time.time()
                self._hits += 1
                return self._cache[user_id]
            self._misses += 1
            return None

    def set(self, user_id: int, data: dict):
        with self._lock:
            if len(self._cache) >= self._max_size and user_id not in self._cache:
                oldest_user = min(self._access_times, key=self._access_times.get)
                del self._cache[oldest_user]
                del self._access_times[oldest_user]
            self._cache[user_id] = data
            self._access_times[user_id] = time.time()

    def invalidate(self, user_id: int):
        with self._lock:
            if user_id in self._cache:
                del self._cache[user_id]
                del self._access_times[user_id]

    def invalidate_user_and_friends(self, user_id: int, friend_ids: list[int]):
        with self._lock:
            all_ids = [user_id] + friend_ids
            for uid in all_ids:
                if uid in self._cache:
                    del self._cache[uid]
                    del self._access_times[uid]

    def clear(self):
        with self._lock:
            self._cache.clear()
            self._access_times.clear()

    def stats(self):
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0
            return {
                "cached_users": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate_percent": round(hit_rate, 2)
            }


recommendation_cache = RecommendationCache(max_size=100)