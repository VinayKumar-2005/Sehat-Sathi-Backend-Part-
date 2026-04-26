# services/risk_engine.py

def calculate_health_risk(profile, family_members):
    """
    Analyzes user profile & family history to calculate risk score.
    Returns: { health_score, risk_score, risk_level, identified_risks }
    """
    risk_score = 0 # Lower is better (0 = Perfect, 100 = Critical)
    risks = []

    # 1. BMI Analysis (Obesity Risk)
    if profile.weight and profile.height:
        bmi = profile.weight / ((profile.height / 100) ** 2)
        if bmi > 30:
            risk_score += 20
            risks.append("Obesity (BMI > 30)")
        elif bmi > 25:
            risk_score += 10
            risks.append("Overweight (BMI > 25)")

    # 2. Blood Pressure Analysis (Hypertension Risk)
    if profile.bp:
        try:
            # Handle formats like "120/80"
            if '/' in profile.bp:
                sys, dia = map(int, profile.bp.split('/'))
                if sys >= 140 or dia >= 90:
                    risk_score += 30
                    risks.append("Hypertension (High BP)")
                elif sys >= 130 or dia >= 85:
                    risk_score += 15
                    risks.append("Pre-Hypertension")
        except:
            pass # Ignore if BP format is invalid

    # 3. Blood Sugar Analysis (Diabetes Risk)
    if profile.sugar:
        if profile.sugar > 140: # Random sugar threshold approx
            risk_score += 30
            risks.append("High Blood Sugar (Diabetes Risk)")
        elif profile.sugar > 110:
            risk_score += 15
            risks.append("Pre-Diabetes Range")

    # 4. Age Factor
    if profile.age > 50:
        risk_score += 10
    elif profile.age > 40:
        risk_score += 5

    # 5. Family History Analysis (Genetic Risk)
    # Check if any family member has specific keywords in their disease list
    has_family_diabetes = any("diabetes" in m.known_diseases.lower() for m in family_members)
    has_family_heart = any("heart" in m.known_diseases.lower() or "bp" in m.known_diseases.lower() for m in family_members)

    if has_family_diabetes:
        risk_score += 15
        risks.append("Family History of Diabetes")
    
    if has_family_heart:
        risk_score += 15
        risks.append("Family History of Heart Disease")

    # --- FINAL CALCULATION ---
    # Cap score at 100
    risk_score = min(risk_score, 100)
    
    # Invert score for "Health Score" (Higher is better, e.g., 90/100)
    health_score = 100 - risk_score

    level = "Low Risk"
    if risk_score > 60:
        level = "High Risk"
    elif risk_score > 30:
        level = "Moderate Risk"

    return {
        "health_score": health_score,
        "risk_score": risk_score,
        "risk_level": level,
        "identified_risks": risks
    }