from mobility_intelligence.schemas import WearableTelemetry
from mobility_intelligence.analytics import generate_mobility_insight
from datetime import datetime

# This is a "test function". Pytest will find it because it starts with "test_"
def test_alert_risk_flag_for_low_gait_symmetry():
    # We create fake wearable data with low gait symmetry
    telemetry = WearableTelemetry(
        patient_id="test_patient",
        timestamp=datetime.now(),
        stride_length_cm=60.0,
        gait_symmetry=0.5,  # This is below 0.7, should trigger alert
        daily_active_minutes=50
    )
    
    # We call our analytics function with this fake data
    result = generate_mobility_insight(telemetry)
    
    # We assert (check) that the result is what we expect
    assert result.risk_flag == "alert"
    assert result.patient_id == "test_patient"

def test_normal_risk_flag_for_good_metrics():
    # This time, good gait symmetry and high activity
    telemetry = WearableTelemetry(
        patient_id="test_patient_2",
        timestamp=datetime.now(),
        stride_length_cm=70.0,
        gait_symmetry=0.9,  # Good symmetry
        daily_active_minutes=100  # High activity
    )
    
    result = generate_mobility_insight(telemetry)
    
    # Should be normal risk
    assert result.risk_flag == "normal"
    assert result.mobility_score > 60