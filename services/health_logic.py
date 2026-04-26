from datetime import datetime

# ... (Helper functions like safe_float, calculate_bmi, calculate_bmr wese hi rahenge) ...
# Agar aapko confusion ho raha hai, toh bas ye poora code replace kar dein:

def safe_float(value):
    try:
        return float(value) if value else 0.0
    except:
        return 0.0

def calculate_bmi(weight, height):
    w = safe_float(weight)
    h = safe_float(height)
    if w == 0 or h == 0: return 0, "Unknown"
    bmi = round(w / ((h/100) ** 2), 1)
    if bmi < 18.5: return bmi, "Underweight"
    elif 18.5 <= bmi < 24.9: return bmi, "Normal"
    elif 25 <= bmi < 29.9: return bmi, "Overweight"
    else: return bmi, "Obese"

def calculate_bmr(weight, height, age, gender):
    w = safe_float(weight)
    h = safe_float(height)
    a = safe_float(age)
    bmr = (10 * w) + (6.25 * h) - (5 * a)
    if gender.lower() == 'male': bmr += 5
    else: bmr -= 161
    return int(bmr)

def check_progress(current_weight, history_logs):
    if not history_logs or len(history_logs) == 0:
        return "Not enough data for history tracking."
    last_log = history_logs[-1]
    diff = current_weight - last_log.weight
    if diff < 0: return f"📉 Great job! You lost {abs(round(diff, 1))} kg since last check."
    elif diff > 0: return f"📈 You gained {round(diff, 1)} kg. Watch your diet."
    else: return "⚖️ Your weight is stable."

def analyze_health(user_data, history_logs=[]):
    # Data extraction
    weight = safe_float(user_data.get('weight'))
    height = safe_float(user_data.get('height'))
    age = safe_float(user_data.get('age', 25))
    gender = user_data.get('gender', 'Male')
    injury = user_data.get('injury', "None")

    report = {
        "status": "Green",
        "conditions_detected": [],
        "risk_score": 0,
        "advice": [],
        "warnings": [],
        "progress_report": "",
        # 👇 YE DO LINES ADD KI HAIN (Fix)
        "age": age,
        "gender": gender
    }

    # 1. BMI Analysis
    bmi, bmi_category = calculate_bmi(weight, height)
    report['bmi'] = bmi
    
    if bmi_category in ["Overweight", "Obese"]:
        report['conditions_detected'].append(f"{bmi_category} (BMI: {bmi})")
        report['risk_score'] += 20

    # 2. Age/Gender Specific Logic
    bmr = calculate_bmr(weight, height, age, gender)
    report['daily_calorie_limit'] = bmr
    
    if age > 50:
        report['warnings'].append("Age 50+: Focus on Joint Health & Calcium.")
        if "High BP" in str(user_data.get('bp')):
             report['risk_score'] += 10
             
    if gender.lower() == 'female' and age > 45:
         report['advice'].append("Consider bone density checkup (Menopause care).")

    # 3. History Tracking
    progress = check_progress(weight, history_logs)
    report['progress_report'] = progress

    # 4. BP & Sugar
    bp_str = user_data.get('bp', "")
    if bp_str and "/" in bp_str:
        try:
            p = bp_str.split('/')
            sys, dia = int(p[0]), int(p[1])
            if sys >= 140 or dia >= 90:
                report['status'] = "Yellow"
                report['conditions_detected'].append(f"High BP ({bp_str})")
                report['advice'].append(f"Strictly limit sodium to <1500mg/day.")
                report['risk_score'] += 30
        except: pass

    sugar = safe_float(user_data.get('sugar'))
    if sugar > 140:
        report['conditions_detected'].append(f"High Sugar ({sugar})")
        report['status'] = "Yellow"
        report['risk_score'] += 30

    # 5. Injury Logic
    if injury and injury.lower() != "none":
        report['conditions_detected'].append(f"Injury: {injury}")
        if "knee" in injury.lower():
             report['warnings'].append("STOP: No Running/Jumping.")

    if report['risk_score'] > 50: report['status'] = "Red"
    elif report['risk_score'] > 0: report['status'] = "Yellow"

    if report['risk_score'] == 0:
        report['advice'].append("You are maintaining good health!")

    return report