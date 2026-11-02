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
    score: Optional[float] = None
    distance: Optional[int] = None
    signals: Optional[dict[str, float]] = None


class RecommendationResponse(BaseModel):
    user_id: int
    algorithm: str
    recommendations: list[RecommendationItem]


class NetworkStats(BaseModel):
    total_users: int
    total_friendships: int


class UserStats(BaseModel):
    user_id: int
    name: str
    friend_count: int


class ConnectionPathUser(BaseModel):
    user_id: int
    name: str


class ConnectionPathResponse(BaseModel):
    user_id: int
    other_user_id: int
    connected: bool
    path: list[ConnectionPathUser]
    degrees: Optional[int] = None
    explanation: str


class NetworkDegreesResponse(BaseModel):
    user_id: int
    first_degree: int
    second_degree: int
    third_degree: int


class MessageResponse(BaseModel):
    message: str


class GraphSnapshotStats(BaseModel):
    loaded: bool
    build_count: int
    nodes: int
    last_build_ms: float
    total_build_ms: float


class CacheStatsResponse(BaseModel):
    cached_users: int
    max_size: int
    hits: int
    misses: int
    hit_rate_percent: float
    graph_snapshot: GraphSnapshotStats


class EndpointMetric(BaseModel):
    method: str
    path: str
    requests: int
    errors: int
    average_ms: float


class RecommendationMetrics(BaseModel):
    count: int
    average_ms: float
    cache_hits: int


class MetricsResponse(BaseModel):
    requests: list[EndpointMetric]
    recommendations: RecommendationMetrics
    recent_average_ms: float


class HealthResponse(BaseModel):
    status: str
    database: str