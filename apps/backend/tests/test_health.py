"""
Tests for the backend API health endpoint
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from src.presentation.api.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Async test client fixture"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


class TestHealthEndpoint:
    """Test cases for the health endpoint"""

    def test_health_endpoint_sync(self, client):
        """Test health endpoint with synchronous client"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_health_endpoint_async(self, async_client):
        """Test health endpoint with asynchronous client"""
        response = await async_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_endpoint_content_type(self, client):
        """Test that health endpoint returns correct content type"""
        response = client.get("/health")

        assert response.headers["content-type"] == "application/json"

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct information"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"


if __name__ == "__main__":
    pytest.main([__file__])
