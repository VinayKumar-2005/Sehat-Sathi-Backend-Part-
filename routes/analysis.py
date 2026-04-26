from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.health_profile import HealthProfile
from models.family_member import FamilyMember 
from models.user import User
from models.workout_plan import WorkoutPlan  # ✅ NEW IMPORT
from extensions import db # ✅ Needed for saving
from services.recommendation import generate_ai_plan 
from services.risk_engine import calculate_health_risk
import json

analysis_bp = Blueprint('analysis_bp', __name__)

# --- SMART AI ROUTE (Saves Plan to DB) ---
@analysis_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_analysis():
    current_identity = get_jwt_identity()
    data = request.get_json() or {}
    force_new = data.get('regenerate', False) # ✅ User can force new plan
    
    # Handle Identity Type (Int vs String)
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id
            
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    # 1. Check if Plan Exists (and user didn't ask to regenerate)
    existing_plan = WorkoutPlan.query.filter_by(user_id=user_id).first()
    
    if existing_plan and not force_new:
        print("⚡ Serving Saved Plan from Database")
        return jsonify(existing_plan.to_dict()['plan']), 200

    # 2. If No Plan or Force New -> Call AI
    print("🤖 Calling AI for New Plan...")
    profile = HealthProfile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        return jsonify({"error": "Profile missing. Please create profile first."}), 404

    try:
        # Generate via AI
        ai_result = generate_ai_plan(profile)
        
        # 3. Save to Database
        if existing_plan:
            existing_plan.plan_data = json.dumps(ai_result) # Update old
            db.session.commit()
        else:
            new_plan = WorkoutPlan(
                user_id=user_id,
                plan_data=json.dumps(ai_result) # Create new
            )
            db.session.add(new_plan)
            db.session.commit()

        return jsonify(ai_result), 200
        
    except Exception as e:
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500


# --- RISK SCORE ROUTE (Unchanged) ---
@analysis_bp.route('/risk-score', methods=['GET'])
@jwt_required()
def get_risk_score():
    """
    Calculates health risk based on Profile + Family History.
    """
    current_identity = get_jwt_identity()
    
    # Resolve User ID
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    if not user_id:
        return jsonify({"error": "User not found"}), 404

    # 1. Get Profile
    profile = HealthProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # 2. Get Family History
    family_members = FamilyMember.query.filter_by(user_id=user_id).all()

    # 3. Calculate Risk
    try:
        risk_data = calculate_health_risk(profile, family_members)
        return jsonify(risk_data), 200
    except Exception as e:
        return jsonify({"error": f"Risk calculation failed: {str(e)}"}), 500