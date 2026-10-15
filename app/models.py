from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    friendships_as_user1 = relationship(
        "Friendship",
        foreign_keys="Friendship.user_id_1",
        back_populates="user1",
        cascade="all, delete-orphan"
    )
    friendships_as_user2 = relationship(
        "Friendship",
        foreign_keys="Friendship.user_id_2",
        back_populates="user2",
        cascade="all, delete-orphan"
    )


class Friendship(Base):
    __tablename__ = "friendships"

    user_id_1 = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user_id_2 = Column(Integer, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user1 = relationship("User", foreign_keys=[user_id_1], back_populates="friendships_as_user1")
    user2 = relationship("User", foreign_keys=[user_id_2], back_populates="friendships_as_user2")

    __table_args__ = (
        CheckConstraint("user_id_1 < user_id_2", name="check_user_id_order"),
        UniqueConstraint("user_id_1", "user_id_2", name="unique_friendship"),
    )