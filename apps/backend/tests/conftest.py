"""Pytest configuration and fixtures."""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")


def pytest_collection_modifyitems(config, items):
    """Skip integration tests if database is not available."""
    if not _is_database_available():
        skip_integration = pytest.mark.skip(reason="Database not available")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


def _is_database_available() -> bool:
    """Check if database is available."""
    database_url = os.getenv("DATABASE_URL", "postgresql://flota_user:flota_password@localhost:5432/flota_db")
    try:
        engine = create_engine(database_url)
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except (OperationalError, Exception):
        return False
