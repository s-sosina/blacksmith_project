import urllib.request
import json

url = "http://127.0.0.1:8000/api/v1/mobility-insights"

data ={
           "patient_id": "pt_12345",
    "timestamp": "2026-08-26T10:00:00Z",
    "stride_length_cm": 65.5,
    "gait_symmetry": 0.65,
    "daily_active_minutes": 45
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as response:
    print(response.status)
    print(json.loads(response.read()))