from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.health_profile import HealthProfile
from models.health_history import HealthHistory
from models.family_member import FamilyMember
from extensions import db
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

# ==========================
# 1. CORE PROFILE (UPDATED)
# ==========================

@profile_bp.route('/create', methods=['POST'])
@jwt_required()
def create_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Handle user ID resolution if identity is email
    if not str(current_user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=current_user_id).first()
        current_user_id = u.id if u else None

    profile = HealthProfile.query.filter_by(user_id=current_user_id).first()
    
    try:
        if profile:
            # Update Existing
            profile.age = data.get('age', profile.age)
            profile.weight = data.get('weight', profile.weight)
            profile.height = data.get('height', profile.height)
            profile.gender = data.get('gender', profile.gender)
            profile.bp = data.get('bp', profile.bp)
            profile.sugar = data.get('sugar', profile.sugar)
            profile.injury = data.get('injury', profile.injury)
            profile.activity_level = data.get('activity_level', profile.activity_level)
            profile.diet_preference = data.get('diet_preference', profile.diet_preference)
            profile.goal = data.get('goal', profile.goal)
            
            # ✅ NEW: Update Context Fields
            profile.workout_environment = data.get('workout_environment', profile.workout_environment)
            profile.experience_level = data.get('experience_level', profile.experience_level)
            
            message = "Profile updated successfully"
        else:
            # Create New
            profile = HealthProfile(
                user_id=current_user_id,
                age=data.get('age'),
                gender=data.get('gender'),
                height=data.get('height'),
                weight=data.get('weight'),
                bp=data.get('bp', '120/80'),
                sugar=data.get('sugar', 90),
                injury=data.get('injury', 'None'),
                activity_level=data.get('activity_level', 'Sedentary'),
                diet_preference=data.get('diet_preference', 'Non-Veg'),
                goal=data.get('goal', 'General Fitness'),
                
                # ✅ NEW: Set Context Fields
                workout_environment=data.get('workout_environment', 'Gym'),
                experience_level=data.get('experience_level', 'Beginner')
            )
            db.session.add(profile)
            message = "Profile created successfully"

        # Also add an entry to History automatically when profile is updated
        new_log = HealthHistory(
            user_id=current_user_id,
            date_logged=datetime.utcnow().date(),
            weight=data.get('weight'),
            note="Profile Update"
        )
        db.session.add(new_log)

        db.session.commit()
        return jsonify({"message": message, "profile": profile.to_dict(), "success": True}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "success": False}), 500

@profile_bp.route('/get', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    
    # Handle user ID resolution
    if not str(current_user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=current_user_id).first()
        current_user_id = u.id if u else None

    profile = HealthProfile.query.filter_by(user_id=current_user_id).first()

    if not profile:
        return jsonify({"message": "Profile not found", "success": False}), 404

    return jsonify({"profile": profile.to_dict(), "success": True}), 200

# ==========================
# 2. MEDICAL TIMELINE 
# ==========================

@profile_bp.route('/history/add', methods=['POST'])
@jwt_required()
def add_history_log():
    """Adds a daily log for Weight, BP, or Sugar"""
    try:
        user_id = get_jwt_identity()
        # Handle user ID resolution
        if not str(user_id).isdigit():
            from models.user import User
            u = User.query.filter_by(email=user_id).first()
            user_id = u.id if u else None
            
        data = request.get_json()

        # FIX: Allow 'sugar_level' to map to 'sugar_random' if specific type is not provided
        sugar_val_random = data.get('sugar_random')
        if sugar_val_random is None and 'sugar_level' in data:
            sugar_val_random = data.get('sugar_level')

        new_log = HealthHistory(
            user_id=user_id,
            date_logged=datetime.utcnow().date(),
            weight=data.get('weight'),
            bp_systolic=data.get('bp_systolic'),
            bp_diastolic=data.get('bp_diastolic'),
            sugar_fasting=data.get('sugar_fasting'),
            sugar_random=sugar_val_random, # Use the mapped value
            note=data.get('note', '')
        )
        
        db.session.add(new_log)
        db.session.commit()
        
        return jsonify({"message": "Health Log added", "log": new_log.to_dict(), "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@profile_bp.route('/history/get', methods=['GET'])
@jwt_required()
def get_history_logs():
    """Fetches last 30 logs"""
    user_id = get_jwt_identity()
    # Handle user ID resolution
    if not str(user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=user_id).first()
        user_id = u.id if u else None

    logs = HealthHistory.query.filter_by(user_id=user_id).order_by(HealthHistory.date_logged.desc()).limit(30).all()
    return jsonify({"history": [log.to_dict() for log in logs], "success": True}), 200

# ==========================
# 3. FAMILY PROFILE
# ==========================

@profile_bp.route('/family/add', methods=['POST'])
@jwt_required()
def add_family_member():
    try:
        user_id = get_jwt_identity()
        # Handle user ID resolution
        if not str(user_id).isdigit():
            from models.user import User
            u = User.query.filter_by(email=user_id).first()
            user_id = u.id if u else None

        data = request.get_json()
        
        member = FamilyMember(
            user_id=user_id,
            name=data.get('name'),
            relation=data.get('relation'),
            age=data.get('age'),
            gender=data.get('gender'),
            known_diseases=data.get('diseases', 'None'),
            allergies=data.get('allergies', 'None')
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify({"message": "Family Member added", "member": member.to_dict(), "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@profile_bp.route('/family/get', methods=['GET'])
@jwt_required()
def get_family_members():
    user_id = get_jwt_identity()
    # Handle user ID resolution
    if not str(user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=user_id).first()
        user_id = u.id if u else None

    members = FamilyMember.query.filter_by(user_id=user_id).all()
    return jsonify({"family": [m.to_dict() for m in members], "success": True}), 200