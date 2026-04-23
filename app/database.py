"""
Database engine + session setup (SQLAlchemy).

Works with either SQLite or PostgreSQL depending on DATABASE_URL in .env.
SQLite needs a special connect_arg (check_same_thread) because it's
normally single-threaded; PostgreSQL doesn't need it.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency-injected DB session (see app/deps.py usage in routers).
    Guarantees the session is closed after each request, even on error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
