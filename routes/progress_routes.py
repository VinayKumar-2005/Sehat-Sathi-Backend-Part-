from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from services.analytics_engine import calculate_consistency_score, get_trend_data

progress_bp = Blueprint('progress_bp', __name__)

@progress_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Returns High-Level Stats for the Dashboard Cards"""
    current_identity = get_jwt_identity()
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    # 1. Calculate Consistency
    score = calculate_consistency_score(user_id)
    
    # 2. Get Score Comment
    comment = "Needs Improvement"
    if score > 80: comment = "Excellent!"
    elif score > 50: comment = "Good"

    return jsonify({
        "consistency_score": score,
        "status": comment,
        "message": f"You have been {score}% consistent this week."
    }), 200

@progress_bp.route('/chart/<metric>', methods=['GET'])
@jwt_required()
def get_chart_data(metric):
    """
    Metric options: 'bp', 'weight', 'sugar'
    Returns JSON ready for Chart.js or Recharts
    """
    current_identity = get_jwt_identity()
    user_id = None
    if str(current_identity).isdigit():
        user_id = int(current_identity)
    else:
        u = User.query.filter_by(email=current_identity).first()
        if u: user_id = u.id

    if metric not in ['bp', 'weight', 'sugar']:
        return jsonify({"error": "Invalid metric. Use bp, weight, or sugar"}), 400

    chart_data = get_trend_data(user_id, metric)
    return jsonify(chart_data), 200