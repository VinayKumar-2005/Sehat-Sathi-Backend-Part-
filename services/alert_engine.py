from models.health_alert import HealthAlert
from extensions import db

def check_vitals_and_alert(user_id, systolic, diastolic, sugar_level):
    """
    Analyzes BP and Sugar. Raises Alerts if thresholds are crossed.
    Returns a list of generated alerts.
    """
    generated_alerts = []

    # --- 1. BLOOD PRESSURE LOGIC ---
    # Normal is approx 120/80. 
    # Hypertensive Crisis is >180/>120.
    if systolic and diastolic:
        sys = int(systolic)
        dia = int(diastolic)

        if sys >= 180 or dia >= 120:
            msg = f"CRITICAL: BP {sys}/{dia} is extremely high (Hypertensive Crisis). Go to a hospital immediately."
            create_alert(user_id, "CRITICAL", "High Blood Pressure", msg)
            generated_alerts.append(msg)
            
        elif sys >= 140 or dia >= 90:
            msg = f"WARNING: BP {sys}/{dia} is high (Hypertension Stage 2). Consult a doctor."
            create_alert(user_id, "HIGH", "High Blood Pressure", msg)
            generated_alerts.append(msg)

    # --- 2. BLOOD SUGAR LOGIC ---
    # Fasting > 126 is Diabetes. > 300 is dangerous. < 70 is Hypoglycemia.
    if sugar_level:
        sugar = int(sugar_level)

        if sugar >= 300:
            msg = f"CRITICAL: Blood Sugar {sugar} mg/dL is very high. Risk of Ketoacidosis."
            create_alert(user_id, "CRITICAL", "High Blood Sugar", msg)
            generated_alerts.append(msg)
            
        elif sugar <= 70:
            msg = f"DANGER: Blood Sugar {sugar} mg/dL is too low (Hypoglycemia). Eat sugar/candy immediately."
            create_alert(user_id, "HIGH", "Low Blood Sugar", msg)
            generated_alerts.append(msg)

    return generated_alerts

def create_alert(user_id, severity, alert_type, message):
    """Internal helper to save alert to DB"""
    try:
        # Check if identical active alert already exists to prevent spam
        existing = HealthAlert.query.filter_by(
            user_id=user_id, 
            alert_type=alert_type, 
            is_active=True
        ).first()

        if existing:
            # Update timestamp instead of creating new duplicate
            existing.message = message
            existing.severity = severity
            db.session.commit()
        else:
            new_alert = HealthAlert(
                user_id=user_id,
                severity=severity,
                alert_type=alert_type,
                message=message
            )
            db.session.add(new_alert)
            db.session.commit()
    except Exception as e:
        print(f"Error saving alert: {e}")