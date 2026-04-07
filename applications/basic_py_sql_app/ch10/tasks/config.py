import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ch10-dev-only-change-in-production")
    WTF_CSRF_TIME_LIMIT = None
    MONGODB_URI = os.environ.get(
        "MONGODB_URI",
        "mongodb://127.0.0.1:27017/tasks",
    )
