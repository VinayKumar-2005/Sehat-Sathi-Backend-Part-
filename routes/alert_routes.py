from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.health_alert import HealthAlert
from services.alert_engine import check_vitals_and_alert

alert_bp = Blueprint('alert_bp', __name__)

@alert_bp.route('/check', methods=['POST'])
@jwt_required()
def trigger_check():
    """
    Manually inputs vitals to check for alerts.
    (In real app, this happens automatically when adding logs)
    """
    current_identity = get_jwt_identity()
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    data = request.get_json()
    systolic = data.get('bp_systolic')
    diastolic = data.get('bp_diastolic')
    sugar = data.get('sugar_level')

    # RUN THE ENGINE
    alerts = check_vitals_and_alert(user_id, systolic, diastolic, sugar)

    if alerts:
        return jsonify({"status": "DANGER", "alerts": alerts}), 200
    else:
        return jsonify({"status": "SAFE", "message": "Vitals are within normal range."}), 200

@alert_bp.route('/active', methods=['GET'])
@jwt_required()
def get_active_alerts():
    """Fetch all active alerts for the user"""
    current_identity = get_jwt_identity()
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    alerts = HealthAlert.query.filter_by(user_id=user_id, is_active=True).all()
    
    return jsonify([a.to_dict() for a in alerts]), 200