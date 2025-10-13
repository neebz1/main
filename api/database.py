"""
Simple in-memory database
For production, replace with SQLAlchemy + PostgreSQL/MySQL
"""

import json
from pathlib import Path
from typing import Any, Dict

# In-memory database (for demo purposes)
# In production, use SQLAlchemy with PostgreSQL/MySQL
_db_storage: Dict[str, Any] = {"users": {}, "items": {}}

# Persistent storage file
DB_FILE = Path(__file__).parent / "data" / "db.json"


def init_db():
    """Initialize database and load from file if exists"""
    global _db_storage

    # Create data directory if it doesn't exist
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing data
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r") as f:
                _db_storage = json.load(f)
            print(f"✅ Loaded database from {DB_FILE}")
        except json.JSONDecodeError:
            print("⚠️  Database file corrupted, starting fresh")
            _db_storage = {"users": {}, "items": {}}
    else:
        print("📝 Creating new database")
        save_db()


def save_db():
    """Save database to file"""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(_db_storage, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving database: {e}")


def get_db():
    """
    Get database instance
    This is a dependency for FastAPI endpoints
    """
    # In production, this would be a database session
    # For now, we return the in-memory storage
    yield _db_storage

    # Save after each request
    save_db()


def clear_db():
    """Clear all data from database"""
    global _db_storage
    _db_storage = {"users": {}, "items": {}}
    save_db()
    print("✅ Database cleared")


def get_stats():
    """Get database statistics"""
    return {
        "total_users": len(_db_storage.get("users", {})),
        "total_items": sum(
            len(items) for items in _db_storage.get("items", {}).values()
        ),
    }


# ==================== MIGRATION TO SQL DATABASE ====================
"""
For production, replace this with SQLAlchemy models:

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    items = relationship("ItemDB", back_populates="owner")

class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="items")

# Database URL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
# Or for SQLite: "sqlite:///./api.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
