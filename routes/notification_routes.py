from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reminder import Reminder
from extensions import db

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/add', methods=['POST'])
@jwt_required()
def add_reminder():
    user_id = get_jwt_identity()
    # Handle email identity if necessary
    if not str(user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=user_id).first()
        user_id = u.id if u else None

    data = request.get_json()
    
    # Validation
    if not data.get('title') or not data.get('time'):
        return jsonify({"error": "Title and Time (HH:MM) are required"}), 400

    new_reminder = Reminder(
        user_id=user_id,
        title=data['title'],
        time_str=data['time'], # Format: "09:30"
        type=data.get('type', 'custom')
    )
    
    db.session.add(new_reminder)
    db.session.commit()
    
    return jsonify({"message": "Reminder set successfully!", "reminder": new_reminder.to_dict()}), 201

@notification_bp.route('/list', methods=['GET'])
@jwt_required()
def list_reminders():
    user_id = get_jwt_identity()
    if not str(user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=user_id).first()
        user_id = u.id if u else None

    reminders = Reminder.query.filter_by(user_id=user_id).all()
    return jsonify({"reminders": [r.to_dict() for r in reminders]}), 200

@notification_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(id):
    user_id = get_jwt_identity()
    # Handle ID resolution
    if not str(user_id).isdigit():
        from models.user import User
        u = User.query.filter_by(email=user_id).first()
        user_id = u.id if u else None

    reminder = Reminder.query.filter_by(id=id, user_id=user_id).first()
    
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
        
    db.session.delete(reminder)
    db.session.commit()
    
    return jsonify({"message": "Reminder deleted"}), 200