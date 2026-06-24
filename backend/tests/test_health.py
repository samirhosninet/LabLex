from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    # Since DB and Redis might be offline/unreachable in a simple unit test run
    # without live services, the endpoint will return HTTP 503 Service Unavailable,
    # but still return a valid health status JSON.
    response = client.get("/api/v1/health")
    assert response.status_code in [200, 503]
    
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert "database" in data["services"]
    assert "redis" in data["services"]
