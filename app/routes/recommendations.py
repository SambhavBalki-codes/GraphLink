from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import services

router = APIRouter(tags=["Stats"])


@router.get("/stats")
def get_network_stats(db: Session = Depends(get_db)):
    return services.get_network_stats(db)


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(__import__('sqlalchemy').text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    return {"status": "ok", "database": db_status}