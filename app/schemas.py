from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserSummary(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class FriendshipCreate(BaseModel):
    user_id_1: int
    user_id_2: int


class FriendshipDelete(BaseModel):
    user_id_1: int
    user_id_2: int


class FriendshipResponse(BaseModel):
    user_id_1: int
    user_id_2: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MutualFriend(BaseModel):
    user_id: int
    name: str


class RecommendationItem(BaseModel):
    user_id: int
    name: str
    mutual_friend_count: int
    mutual_friends: list[MutualFriend]
    reason: str


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: list[RecommendationItem]


class NetworkStats(BaseModel):
    total_users: int
    total_friendships: int


class UserStats(BaseModel):
    user_id: int
    name: str
    friend_count: int


class HealthResponse(BaseModel):
    status: str
    database: str