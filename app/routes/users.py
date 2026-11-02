from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.schemas import (
    ConnectionPathResponse,
    MessageResponse,
    NetworkDegreesResponse,
    RecommendationResponse,
    UserCreate,
    UserResponse,
    UserStats,
    UserSummary,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db, user.name, user.email, user.company, user.location, user.education, user.bio)


@router.get("", response_model=list[UserResponse])
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return services.get_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return services.get_user_or_404(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    return services.update_user(db, user_id, update_data)


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return services.delete_user(db, user_id)


@router.get("/{user_id}/friends", response_model=list[UserSummary])
def get_friends(user_id: int, db: Session = Depends(get_db)):
    return services.get_user_friends(db, user_id)


@router.get("/{user_id}/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    user_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    algorithm: str = Query(default="v2"),
    db: Session = Depends(get_db)
):
    return services.get_friend_recommendations_v2(db, user_id, limit, algorithm)


@router.get("/{user_id}/path/{other_user_id}", response_model=ConnectionPathResponse)
def get_connection_path(
    user_id: int,
    other_user_id: int,
    db: Session = Depends(get_db)
):
    return services.get_connection_path(db, user_id, other_user_id)


@router.get("/{user_id}/network", response_model=NetworkDegreesResponse)
def get_network_degrees(user_id: int, db: Session = Depends(get_db)):
    return services.get_network_degrees(db, user_id)


@router.get("/{user_id}/stats", response_model=UserStats)
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    return services.get_user_stats(db, user_id)