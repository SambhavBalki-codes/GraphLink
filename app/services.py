from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import crud
from app.graph import build_adjacency_list, get_recommendations, bfs_distances
from app.cache import recommendation_cache


def get_user_or_404(db: Session, user_id: int):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


def create_user(db: Session, name: str, email: str, company: str = None, location: str = None, education: str = None, bio: str = None):
    existing = crud.get_user_by_email(db, email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    from app.schemas import UserCreate
    return crud.create_user(db, UserCreate(name=name, email=email, company=company, location=location, education=education, bio=bio))


def get_users(db: Session, skip: int = 0, limit: int = 20):
    return crud.get_users(db, skip=skip, limit=limit)


def update_user(db: Session, user_id: int, update_data):
    get_user_or_404(db, user_id)
    data = {k: v for k, v in update_data.model_dump().items() if v is not None}
    return crud.update_user(db, user_id, data)


def delete_user(db: Session, user_id: int):
    get_user_or_404(db, user_id)
    crud.delete_user(db, user_id)
    recommendation_cache.invalidate(user_id)
    return {"message": f"User {user_id} deleted successfully"}


def create_friendship(db: Session, user_id_1: int, user_id_2: int):
    if user_id_1 == user_id_2:
        raise HTTPException(status_code=400, detail="Users cannot be friends with themselves")
    get_user_or_404(db, user_id_1)
    get_user_or_404(db, user_id_2)
    existing = crud.get_friendship(db, user_id_1, user_id_2)
    if existing:
        raise HTTPException(status_code=409, detail="Friendship already exists")
    result = crud.create_friendship(db, user_id_1, user_id_2)
    recommendation_cache.invalidate_user_and_friends(user_id_1, [user_id_2])
    return result


def delete_friendship(db: Session, user_id_1: int, user_id_2: int):
    get_user_or_404(db, user_id_1)
    get_user_or_404(db, user_id_2)
    friendship = crud.get_friendship(db, user_id_1, user_id_2)
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    crud.delete_friendship(db, user_id_1, user_id_2)
    recommendation_cache.invalidate_user_and_friends(user_id_1, [user_id_2])
    return {"message": "Friendship deleted successfully"}


def get_user_friends(db: Session, user_id: int):
    get_user_or_404(db, user_id)
    return crud.get_user_friends(db, user_id)


def get_friend_recommendations(db: Session, user_id: int, limit: int = 10):
    user = get_user_or_404(db, user_id)
    all_friendships = crud.get_all_friendships(db)
    friendship_pairs = [(f.user_id_1, f.user_id_2) for f in all_friendships]
    graph = build_adjacency_list(friendship_pairs)
    raw_recommendations = get_recommendations(user_id, graph, limit)
    result = []
    for rec in raw_recommendations:
        candidate = crud.get_user(db, rec["candidate_id"])
        if not candidate:
            continue
        mutual_friends = []
        for mf_id in rec["mutual_friends"]:
            mf_user = crud.get_user(db, mf_id)
            if mf_user:
                mutual_friends.append({"user_id": mf_user.id, "name": mf_user.name})
        count = rec["mutual_friend_count"]
        result.append({
            "user_id": candidate.id,
            "name": candidate.name,
            "mutual_friend_count": count,
            "mutual_friends": mutual_friends,
            "reason": f"You share {count} mutual friend{'s' if count > 1 else ''}."
        })
    return {"user_id": user_id, "recommendations": result}


def get_friend_recommendations_v2(db: Session, user_id: int, limit: int = 10, algorithm: str = "v2"):
    user = get_user_or_404(db, user_id)

    cache_key = f"{user_id}_{limit}_{algorithm}"
    cached = recommendation_cache.get(user_id)
    if cached and cached.get("cache_key") == cache_key:
        return cached["data"]

    all_friendships = crud.get_all_friendships(db)
    friendship_pairs = [(f.user_id_1, f.user_id_2) for f in all_friendships]
    graph = build_adjacency_list(friendship_pairs)
    use_multi_signal = algorithm != "v1"
    raw_recommendations = get_recommendations(user_id, graph, limit, use_multi_signal)

    result = []
    for rec in raw_recommendations:
        candidate = crud.get_user(db, rec["candidate_id"])
        if not candidate:
            continue
        mutual_friends = []
        for mf_id in rec["mutual_friends"]:
            mf_user = crud.get_user(db, mf_id)
            if mf_user:
                mutual_friends.append({"user_id": mf_user.id, "name": mf_user.name})
        count = rec["mutual_friend_count"]
        result.append({
            "user_id": candidate.id,
            "name": candidate.name,
            "mutual_friend_count": count,
            "mutual_friends": mutual_friends,
            "score": rec["score"],
            "distance": rec["distance"],
            "reason": f"You share {count} mutual friend{'s' if count > 1 else ''}."
        })

    response = {"user_id": user_id, "algorithm": algorithm, "recommendations": result}
    recommendation_cache.set(user_id, {"cache_key": cache_key, "data": response})
    return response


def get_connection_path(db: Session, user_id: int, other_user_id: int):
    get_user_or_404(db, user_id)
    get_user_or_404(db, other_user_id)
    all_friendships = crud.get_all_friendships(db)
    friendship_pairs = [(f.user_id_1, f.user_id_2) for f in all_friendships]
    graph = build_adjacency_list(friendship_pairs)
    from app.graph import bfs_path
    path_ids = bfs_path(user_id, other_user_id, graph)
    if not path_ids:
        return {
            "user_id": user_id,
            "other_user_id": other_user_id,
            "connected": False,
            "path": [],
            "degrees": None,
            "explanation": "No connection found between these users."
        }
    path_users = []
    for pid in path_ids:
        u = crud.get_user(db, pid)
        if u:
            path_users.append({"user_id": u.id, "name": u.name})
    degrees = len(path_ids) - 1
    names = [u["name"] for u in path_users]
    explanation = " → ".join(names)
    return {
        "user_id": user_id,
        "other_user_id": other_user_id,
        "connected": True,
        "path": path_users,
        "degrees": degrees,
        "explanation": explanation
    }


def get_network_degrees(db: Session, user_id: int):
    get_user_or_404(db, user_id)
    all_friendships = crud.get_all_friendships(db)
    friendship_pairs = [(f.user_id_1, f.user_id_2) for f in all_friendships]
    graph = build_adjacency_list(friendship_pairs)
    from app.graph import get_network_degrees as graph_network_degrees
    degrees = graph_network_degrees(user_id, graph)
    return {
        "user_id": user_id,
        "first_degree": degrees["first"],
        "second_degree": degrees["second"],
        "third_degree": degrees["third"]
    }


def get_network_stats(db: Session):
    return {
        "total_users": crud.get_total_users(db),
        "total_friendships": crud.get_total_friendships(db)
    }


def get_user_stats(db: Session, user_id: int):
    user = get_user_or_404(db, user_id)
    friend_count = len(crud.get_user_friends(db, user_id))
    return {
        "user_id": user_id,
        "name": user.name,
        "friend_count": friend_count
    }


def get_bfs_distances(db: Session, user_id: int):
    get_user_or_404(db, user_id)
    all_friendships = crud.get_all_friendships(db)
    friendship_pairs = [(f.user_id_1, f.user_id_2) for f in all_friendships]
    graph = build_adjacency_list(friendship_pairs)
    return bfs_distances(user_id, graph)