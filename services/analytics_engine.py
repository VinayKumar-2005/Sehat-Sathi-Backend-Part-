from models.health_history import HealthHistory
from models.workout_log import WorkoutLog
from datetime import datetime, timedelta
from sqlalchemy import func

def calculate_consistency_score(user_id):
    """
    Calculates a score (0-100) based on logging frequency in the last 7 days.
    """
    # Get current date (not datetime) to match DB column type
    today = datetime.utcnow().date()
    seven_days_ago = today - timedelta(days=7)

    # Count days with at least one Health Log
    # FIX: Using 'date_logged' as defined in your model
    health_logs = HealthHistory.query.filter(
        HealthHistory.user_id == user_id,
        HealthHistory.date_logged >= seven_days_ago
    ).count()

    # Count days with at least one Workout
    # WorkoutLog uses 'date' (this is correct based on your model)
    workout_logs = WorkoutLog.query.filter(
        WorkoutLog.user_id == user_id,
        WorkoutLog.date >= seven_days_ago
    ).count()

    total_activity = health_logs + workout_logs
    
    # Logic: If they did 5+ activities in 7 days, they are 100% consistent.
    score = min((total_activity / 5) * 100, 100)
    return round(score)

def get_trend_data(user_id, metric="bp"):
    """
    Returns data formatted for Frontend Charts (Line Charts).
    """
    # Get last 30 entries
    # FIX: Using 'date_logged' for sorting
    logs = HealthHistory.query.filter_by(user_id=user_id)\
        .order_by(HealthHistory.date_logged.asc()).limit(30).all()

    labels = [] # Dates
    values = [] # The metric data

    for log in logs:
        # Format Date (e.g., "12 Oct")
        # FIX: Using 'date_logged'
        date_str = log.date_logged.strftime("%d %b")
        
        if metric == "bp":
            if log.bp_systolic and log.bp_diastolic:
                labels.append(date_str)
                values.append({
                    "systolic": log.bp_systolic,
                    "diastolic": log.bp_diastolic
                })
        elif metric == "weight":
            if log.weight:
                labels.append(date_str)
                values.append(log.weight)
        elif metric == "sugar":
            # FIX: Your model has sugar_fasting and sugar_random.
            # We will use Random sugar for general trending, or Fasting if Random is missing.
            val = log.sugar_random if log.sugar_random else log.sugar_fasting
            if val:
                labels.append(date_str)
                values.append(val)

    return {
        "labels": labels,
        "data": values,
        "title": f"{metric.upper()} Trends (Last 30 Logs)"
    }