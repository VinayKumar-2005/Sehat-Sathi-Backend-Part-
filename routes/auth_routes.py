from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token
from utils.response_utils import success_response, error_response

auth_bp = Blueprint('auth', __name__) # URL prefix app.py me handle ho raha hai, yahan hata diya to avoid double //

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return error_response("Missing required fields", 400)

    if User.query.filter_by(email=email).first():
        return error_response("Email already exists", 409)

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return success_response("User registered successfully", {"user": new_user.to_dict()}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Cast ID to string for JWT compatibility
        access_token = create_access_token(identity=str(user.id))
        
        # ✅ FIX: Return standard JWT response (Root level access_token)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict(),
            "success": True
        }), 200
    
    return error_response("Invalid email or password", 401)