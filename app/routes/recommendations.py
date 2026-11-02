from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import services
from app.cache import graph_snapshot_cache, recommendation_cache
from app.observability import metrics
from app.schemas import CacheStatsResponse, HealthResponse, MetricsResponse, NetworkStats

router = APIRouter(tags=["Stats"])


@router.get("/stats", response_model=NetworkStats)
def get_network_stats(db: Session = Depends(get_db)):
    return services.get_network_stats(db)


@router.get("/cache/stats", response_model=CacheStatsResponse)
def get_cache_stats():
    return {
        **recommendation_cache.stats(),
        "graph_snapshot": graph_snapshot_cache.stats()
    }


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    return metrics.snapshot()


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(__import__('sqlalchemy').text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    return {"status": "ok", "database": db_status}