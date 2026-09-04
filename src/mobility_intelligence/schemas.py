from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

# Input: What the wearable device sends us
class WearableTelemetry(BaseModel):
    patient_id: str
    timestamp: datetime
    stride_length_cm: float = Field(gt=0, lt=200) # Must be greater than 0, less than 200
    gait_symmetry: float = Field(ge=0.0, le=1.0)  # Must be between 0.0 and 1.0
    daily_active_minutes: int = Field(ge=0)       # Must be 0 or greater

# Output: What we send back to the clinician
class MobilityInsight(BaseModel):
    patient_id: str
    mobility_score: int = Field(ge=0, le=100)
    risk_flag: Literal["normal", "monitor", "alert"]
    clinician_summary: str