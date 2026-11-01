from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    bio: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    company: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    bio: Optional[str] = None
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