from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import User, Friendship
from app.schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_friendship(db: Session, user_id_1: int, user_id_2: int):
    small_id = min(user_id_1, user_id_2)
    large_id = max(user_id_1, user_id_2)
    return db.query(Friendship).filter(
        Friendship.user_id_1 == small_id,
        Friendship.user_id_2 == large_id
    ).first()


def create_friendship(db: Session, user_id_1: int, user_id_2: int):
    small_id = min(user_id_1, user_id_2)
    large_id = max(user_id_1, user_id_2)
    friendship = Friendship(user_id_1=small_id, user_id_2=large_id)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


def delete_friendship(db: Session, user_id_1: int, user_id_2: int):
    friendship = get_friendship(db, user_id_1, user_id_2)
    if friendship:
        db.delete(friendship)
        db.commit()
    return friendship


def get_user_friendships(db: Session, user_id: int):
    return db.query(Friendship).filter(
        or_(
            Friendship.user_id_1 == user_id,
            Friendship.user_id_2 == user_id
        )
    ).all()


def get_user_friends(db: Session, user_id: int):
    friendships = get_user_friendships(db, user_id)
    friend_ids = []
    for f in friendships:
        if f.user_id_1 == user_id:
            friend_ids.append(f.user_id_2)
        else:
            friend_ids.append(f.user_id_1)
    if not friend_ids:
        return []
    return db.query(User).filter(User.id.in_(friend_ids)).all()


def get_all_friendships(db: Session):
    return db.query(Friendship).all()


def get_total_users(db: Session):
    return db.query(User).count()


def get_total_friendships(db: Session):
    return db.query(Friendship).count()