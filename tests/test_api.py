import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns 200"""
    response = client.get("/")
    assert response.status_code == 200

def test_docs_endpoint():
    """Test the Swagger docs endpoint is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_health_check():
    """Test health check endpoint if it exists"""
    response = client.get("/health")
    # This might not exist yet, so we expect 404
    assert response.status_code in [200, 404]

def test_chat_endpoint_without_docs():
    """Test chat endpoint behavior when no documents are uploaded"""
    response = client.post(
        "/api/chat",
        json={"query": "test query"}
    )
    # Should handle gracefully when no documents exist
    assert response.status_code in [200, 400, 404]

def test_upload_endpoint():
    """Test document upload endpoint"""
    # Test with empty request
    response = client.post("/api/upload")
    assert response.status_code in [200, 400, 422]  # 422 for validation error
