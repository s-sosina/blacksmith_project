from .schemas import WearableTelemetry, MobilityInsight

def generate_mobility_insight(telemetry: WearableTelemetry) -> MobilityInsight:
    # 1. Calculate a mock mobility score (0 to 100)
    # We give up to 50 points for good gait symmetry, and up to 50 points for daily activity.
    symmetry_points = telemetry.gait_symmetry * 50
    activity_points = min(telemetry.daily_active_minutes / 2, 50) # Caps at 50 points
    total_score = int(symmetry_points + activity_points)
    
    # 2. Determine risk flag and summary based on the data
    if telemetry.gait_symmetry < 0.7:
        risk = "alert"
        summary = "Significant gait asymmetry detected. Recommend immediate clinical review."
    elif total_score < 60:
        risk = "monitor"
        summary = "Mobility score below baseline. Monitor for downward trend."
    else:
        risk = "normal"
        summary = "Mobility metrics within expected rehabilitation parameters."

    # 3. Return the structured insight
    return MobilityInsight(
        patient_id=telemetry.patient_id,
        mobility_score=total_score,
        risk_flag=risk,
        clinician_summary=summary
    )