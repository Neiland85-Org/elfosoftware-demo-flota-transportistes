"""
Database session configuration for SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for development/testing

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)
