import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_reject_without_feedback_raises_400():
    payload = {
        "thread_id": "test_thread_abc",
        "approved": False,
        "feedback": "   "
    }
    response = client.post("/api/travel/approve", json=payload)
    assert response.status_code == 400
    assert "feedback" in response.json()["detail"].lower()


@patch("app.api.routes.run_travel_agent")
def test_create_trip_endpoint(mock_run):
    mock_run.return_value = {
        "thread_id": "test_thread_123",
        "answer": "Draft Itinerary",
        "requires_approval": True,
    }

    payload = {"message": "Plan a trip to Rome"}
    response = client.post("/api/travel", json=payload)

    assert response.status_code == 200
    assert response.json()["thread_id"] == "test_thread_123"