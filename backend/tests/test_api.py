from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_required_inputs() -> None:
    response = client.get("/api/required-inputs")
    assert response.status_code == 200
    payload = response.json()
    assert "ingestion" in payload
    assert any(item["key"] == "title" for item in payload["ingestion"])
