from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.health_history import HealthHistory
from models.health_profile import HealthProfile # To update current profile too
from services.health_logic import analyze_health
from services.recommendation import get_recommendations
from utils.validators import validate_health_data
from utils.response_formatter import success_response, error_response
import json

health_bp = Blueprint('health', __name__)

@health_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_health_data():
    user_id = get_jwt_identity()
    data = request.get_json()

    # 1. Security & Validation Layer
    validation_errors = validate_health_data(data)
    if validation_errors:
        return error_response("Invalid Health Data", 400, validation_errors)

    # 2. Logic Layer (The Doctor)
    # Hum dummy logs pass kar rahe hain abhi ke liye, Phase 2 mein real history pass karenge
    analysis_report = analyze_health(data, history_logs=[]) 
    
    # 3. Recommendation Layer
    diet_workout_plan = get_recommendations(analysis_report['conditions_detected'])

    # 4. Persistence Layer (Save to History & Update Profile)
    
    # Update Current Profile (Latest State)
    # (Yahan hum check karte hain agar profile hai to update, nahi to create - Short logic)
    profile = HealthProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = HealthProfile(user_id=user_id, **{k:v for k,v in data.items() if k in ['height','weight','age','gender']})
        db.session.add(profile)
    else:
        profile.weight = data.get('weight', profile.weight)
        # ... other fields update
    
    # Save History Snapshot (Permanent Record)
    history_entry = HealthHistory(
        user_id=user_id,
        age=data.get('age'),
        weight=data.get('weight'),
        height=data.get('height'),
        bp=data.get('bp'),
        sugar=data.get('sugar'),
        injury=data.get('injury'),
        bmi=analysis_report.get('bmi'),
        status=analysis_report.get('status'),
        risk_score=analysis_report.get('risk_score'),
        conditions_detected=json.dumps(analysis_report.get('conditions_detected')),
        recommendations_summary=json.dumps(analysis_report.get('advice'))
    )
    
    db.session.add(history_entry)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database Error: {str(e)}", 500)

    # 5. Response Layer
    final_response = {
        "report_id": history_entry.id, # Future mein AI explanation ke liye kaam aayega
        "analysis": analysis_report,
        "plan": diet_workout_plan
    }
    
    return success_response("Health Analysis Complete", final_response)