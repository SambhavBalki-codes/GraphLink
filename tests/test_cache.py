import time

from app.cache import RecommendationCache


def test_recommendation_cache_expires_entries():
    cache = RecommendationCache(max_size=2, ttl_seconds=0.01)
    cache.set((1, 10, "v2"), {"value": "cached"})

    assert cache.get((1, 10, "v2")) == {"value": "cached"}
    time.sleep(0.02)
    assert cache.get((1, 10, "v2")) is None
    assert cache.stats()["expirations"] == 1


def test_recommendation_cache_evicts_least_recently_used_entry():
    cache = RecommendationCache(max_size=2, ttl_seconds=60)
    cache.set((1, 10, "v2"), {"value": 1})
    cache.set((2, 10, "v2"), {"value": 2})
    assert cache.get((1, 10, "v2")) == {"value": 1}

    cache.set((3, 10, "v2"), {"value": 3})

    assert cache.get((1, 10, "v2")) == {"value": 1}
    assert cache.get((2, 10, "v2")) is None
    assert cache.stats()["evictions"] == 1


def test_recommendation_cache_keeps_algorithm_variants_separate():
    cache = RecommendationCache(max_size=2, ttl_seconds=60)
    cache.set((1, 10, "v1"), {"algorithm": "v1"})
    cache.set((1, 10, "v2"), {"algorithm": "v2"})

    assert cache.get((1, 10, "v1"))["algorithm"] == "v1"
    assert cache.get((1, 10, "v2"))["algorithm"] == "v2"
