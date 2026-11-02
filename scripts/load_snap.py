import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from app.database import SessionLocal
from app.models import Friendship, User

DATA_FILE = "data/facebook_combined.txt"


def load_snap_dataset():
    db = SessionLocal()

    try:
        print("Clearing existing data...")
        db.execute(text("DELETE FROM friendships"))
        db.execute(text("DELETE FROM users"))
        db.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        db.commit()

        print("Reading dataset...")
        edges = []
        node_ids = set()

        with open(DATA_FILE, "r") as f:
            for line in f:
                a, b = map(int, line.strip().split())
                node_ids.add(a)
                node_ids.add(b)
                edges.append((a, b))

        print(f"Found {len(node_ids)} users and {len(edges)} friendships")

        print("Creating users...")
        node_list = sorted(node_ids)
        for node_id in node_list:
            user = User(
                name=f"User_{node_id}",
                email=f"user_{node_id}@facebook.snap"
            )
            db.add(user)

        db.commit()
        print(f"Created {len(node_list)} users")

        print("Loading user ID mapping...")
        users = db.query(User).all()
        email_to_id = {u.email: u.id for u in users}

        print("Creating friendships...")
        count = 0
        for a, b in edges:
            small = min(a, b)
            large = max(a, b)
            email_1 = f"user_{small}@facebook.snap"
            email_2 = f"user_{large}@facebook.snap"
            uid1 = email_to_id.get(email_1)
            uid2 = email_to_id.get(email_2)
            if uid1 and uid2 and uid1 != uid2:
                friendship = Friendship(user_id_1=min(uid1, uid2), user_id_2=max(uid1, uid2))
                db.add(friendship)
                count += 1
                if count % 5000 == 0:
                    db.commit()
                    print(f"  {count} friendships loaded...")

        db.commit()
        print(f"Created {count} friendships")
        print("Stanford SNAP dataset loaded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_snap_dataset()