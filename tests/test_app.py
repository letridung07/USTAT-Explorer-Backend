from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_metadata() -> None:
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "USTAT Explorer Backend"
    assert payload["version"] == "0.1.0"
    assert payload["environment"] == "development"


def test_health_returns_ok_status() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
