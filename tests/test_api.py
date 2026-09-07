from fastapi.testclient import TestClient

from blacksmith_service.main import app

client = TestClient(app)


def test_message_endpoint_echoes_and_confirms():
    response = client.post("/api/v1/messages", json={"message": "hello"})

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "hello"
    assert body["processed"] is True
    assert body["status"] == "received"


def test_message_endpoint_rejects_missing_message():
    response = client.post("/api/v1/messages", json={})

    assert response.status_code == 400
    assert response.json()["detail"] == "Message is required"


def test_message_endpoint_rejects_empty_message():
    response = client.post("/api/v1/messages", json={"message": ""})

    assert response.status_code == 400
    assert response.json()["detail"] == "Message is required"


def test_message_endpoint_rejects_missing_body():
    # No json= at all -> no request body, not just an empty dict.
    response = client.post("/api/v1/messages")

    assert response.status_code == 400
    assert response.json()["detail"] == "Message is required"
