"""
Tests for health endpoint
"""
import pytest
from fastapi.testclient import TestClient
from src.presentation.api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health endpoint returns ok status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint():
    """Test root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Elfosoftware Demo" in data["message"]
    assert data["status"] == "running"

def test_api_v1_endpoint():
    """Test API v1 endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "API v1"
    assert data["version"] == "0.1.0"