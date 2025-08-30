"""Integration tests for database connectivity."""

import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from infrastructure.persistence.session import SessionLocal, engine


@pytest.mark.integration
def test_database_connection():
    """Test that we can connect to the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1
    except OperationalError:
        pytest.skip("Database not available - skipping integration test")


@pytest.mark.integration
def test_session_creation():
    """Test that we can create and use a database session."""
    try:
        db = SessionLocal()
        # Simple query to test session
        result = db.execute(text("SELECT version()"))
        version = result.fetchone()
        assert version is not None
        db.close()
    except OperationalError:
        pytest.skip("Database not available - skipping integration test")
