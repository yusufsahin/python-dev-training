import os

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.security import hash_password


def main() -> None:
    if os.environ.get("SEED_DEMO_USER", "").lower() not in ("1", "true", "yes"):
        return
    db = SessionLocal()
    try:
        demo = db.scalar(select(User).where(User.username == "demo"))
        if demo:
            demo.email = "demo@storium.local"
            demo.hashed_password = hash_password("storium-demo-2024")
            demo.is_active = True
        else:
            db.add(
                User(
                    email="demo@storium.local",
                    username="demo",
                    hashed_password=hash_password("storium-demo-2024"),
                    is_active=True,
                ),
            )
        db.commit()
        print("Identity demo user OK.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
