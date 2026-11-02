from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.schemas import (
    FriendshipCreate,
    FriendshipDelete,
    FriendshipResponse,
    MessageResponse,
)

router = APIRouter(prefix="/friendships", tags=["Friendships"])


@router.post("", response_model=FriendshipResponse, status_code=201)
def create_friendship(friendship: FriendshipCreate, db: Session = Depends(get_db)):
    return services.create_friendship(db, friendship.user_id_1, friendship.user_id_2)


@router.delete("", response_model=MessageResponse)
def delete_friendship(friendship: FriendshipDelete, db: Session = Depends(get_db)):
    return services.delete_friendship(db, friendship.user_id_1, friendship.user_id_2)