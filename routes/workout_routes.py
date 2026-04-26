from flask import Blueprint, request, jsonify
from extensions import db
from models.workout_log import WorkoutLog
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

workout_bp = Blueprint('workout', __name__)

# 1. LOG A WORKOUT (User saves what they did)
@workout_bp.route('/log', methods=['POST'])
@jwt_required()
def log_workout():
    current_identity = get_jwt_identity()
    
    # Handle User ID resolution
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    if not user_id:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    
    # Validate required fields
    if not data.get('exercise_name') or not data.get('sets') or not data.get('reps'):
        return jsonify({"error": "Missing exercise details"}), 400

    new_log = WorkoutLog(
        user_id=user_id,
        exercise_name=data['exercise_name'],
        sets_done=int(data['sets']),
        reps_done=int(data['reps']),
        weight_kg=float(data.get('weight', 0)), # Default to 0 if empty
        notes=data.get('notes', ''),
        date=datetime.utcnow().date() # Auto-set today's date
    )

    try:
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Workout logged successfully!", "log": new_log.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 2. VIEW WORKOUT HISTORY (Show past logs)
@workout_bp.route('/history', methods=['GET'])
@jwt_required()
def get_workout_history():
    current_identity = get_jwt_identity()
    
    # Handle User ID resolution
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    # Fetch last 10 logs, newest first
    logs = WorkoutLog.query.filter_by(user_id=user_id).order_by(WorkoutLog.date.desc(), WorkoutLog.id.desc()).limit(20).all()
    
    return jsonify({
        "count": len(logs),
        "history": [log.to_dict() for log in logs]
    }), 200