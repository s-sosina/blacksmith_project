from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_mobility_insights_endpoint():
    data = {
        "patient_id": "pt_12345",
        "timestamp": "2026-08-26T10:00:00Z",
        "stride_length_cm": 65.5,
        "gait_symmetry": 0.65,
        "daily_active_minutes": 45,
    }

    response = client.post("/api/v1/mobility-insights", json=data)

    assert response.status_code == 200
    body = response.json()
    assert body["patient_id"] == "pt_12345"
    assert body["risk_flag"] == "alert"
    assert "mobility_score" in body
    assert "clinician_summary" in body
