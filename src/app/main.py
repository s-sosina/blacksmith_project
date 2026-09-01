from fastapi import FastAPI
from .schemas import WearableTelemetry, MobilityInsight
from .analytics import generate_mobility_insight

app = FastAPI(title="Wearable Telemetry API")

@app.get("/health")
async def health_check():
    """Health check endpoint for service monitoring."""
    return {"status": "ok", "service": "blacksmith_project"}

@app.post("/api/v1/mobility-insights", response_model=MobilityInsight)
async def analyze_telemetry(telemetry: WearableTelemetry):
    return generate_mobility_insight(telemetry)