from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from extensions import db # 🟢 NEW: Database operations ke liye zaroori hai

# Models
from models.user import User
from models.health_profile import HealthProfile
from models.chat_log import ChatLog
from models.health_history import HealthHistory

# Services & Utils
from services.ai_doctor import get_ai_response, save_chat
from utils.api_helpers import api_response
from utils.logger import app_logger # ✅ NEW: Import Logger

chat_bp = Blueprint('chat_bp', __name__)

# ✅ NEW: Mandatory Medical Disclaimer
MEDICAL_DISCLAIMER = "\n\n(Note: I am an AI, not a doctor. Please consult a professional for medical advice.)"

@chat_bp.route('/ask', methods=['POST'])
@jwt_required()
def send_message():
    try:
        current_identity = get_jwt_identity()
        
        # --- 1. User Resolution ---
        user_id = None
        if str(current_identity).isdigit():
            user_id = int(current_identity)
        else:
            u = User.query.filter_by(email=current_identity).first()
            if u: user_id = u.id
            
        if not user_id:
            return api_response(False, "User not found", status_code=404)

        # --- 2. Input Validation ---
        data = request.get_json()
        if not data:
            return api_response(False, "No input data provided", status_code=400)
            
        user_message = data.get('message', '').strip()
        if not user_message:
            return api_response(False, "Message cannot be empty", status_code=400)

        # Log Interaction (Non-PII)
        app_logger.info(f"User {user_id} sent a chat message.")

        # --- 3. Build Memory Context ---
        
        # A. Profile
        profile = HealthProfile.query.filter_by(user_id=user_id).first()
        
        # B. Chat History (Last 6 messages)
        recent_chats = ChatLog.query.filter_by(user_id=user_id)\
            .order_by(desc(ChatLog.timestamp))\
            .limit(6).all()
        
        chat_history_text = ""
        for chat in reversed(recent_chats):
            sender_label = "Patient" if chat.sender == "user" else "AI Caretaker"
            chat_history_text += f"{sender_label}: {chat.message}\n"

        # C. Health History (Last 3 logs)
        recent_health = HealthHistory.query.filter_by(user_id=user_id)\
            .order_by(desc(HealthHistory.date_logged))\
            .limit(3).all()
            
        health_context_text = "RECENT HEALTH LOGS:\n"
        if recent_health:
            for log in recent_health:
                log_dict = log.to_dict()
                health_context_text += f"- Date: {log_dict['date']}, BP: {log_dict['bp']}, Sugar: {log_dict['sugar']}\n"
        else:
            health_context_text += "No recent health logs available.\n"

        # --- 4. Construct Prompt ---
        full_context_prompt = (
            f"{health_context_text}\n"
            f"RECENT CONVERSATION:\n{chat_history_text}\n"
            f"CURRENT PATIENT MESSAGE: {user_message}\n"
            f"INSTRUCTION: Answer empathetically. Use health logs if relevant. Keep it short."
        )

        # --- 5. Save & Process ---
        
        # Save User Message
        save_chat(user_id, "user", user_message)

        # Get AI Response
        ai_reply = get_ai_response(user_id, full_context_prompt, profile)
        
        # ✅ SAFETY CHECK: Append Disclaimer if not present
        if "AI, not a doctor" not in ai_reply:
             ai_reply += MEDICAL_DISCLAIMER

        # Save AI Response
        save_chat(user_id, "ai", ai_reply)

        return api_response(True, "Message processed", {
            "user_message": user_message,
            "ai_response": ai_reply
        })

    except Exception as e:
        app_logger.error(f"Chat Error: {str(e)}") # ✅ Log to file
        return api_response(False, "An internal error occurred", status_code=500)

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        current_identity = get_jwt_identity()
        user_id = None
        if str(current_identity).isdigit():
            user_id = int(current_identity)
        else:
            u = User.query.filter_by(email=current_identity).first()
            if u: user_id = u.id

        if not user_id:
            return api_response(False, "User not found", status_code=404)

        logs = ChatLog.query.filter_by(user_id=user_id).order_by(ChatLog.timestamp.asc()).limit(50).all()
        
        return api_response(True, "History fetched", [log.to_dict() for log in logs])
    
    except Exception as e:
        app_logger.error(f"History Error: {str(e)}") # ✅ Log to file
        return api_response(False, "Error fetching history", status_code=500)


# 🟢 NEW: API route to DELETE Chat History
@chat_bp.route('/history', methods=['DELETE'])
@jwt_required()
def delete_history():
    try:
        current_identity = get_jwt_identity()
        user_id = None
        
        # User ID resolve karna
        if str(current_identity).isdigit():
            user_id = int(current_identity)
        else:
            u = User.query.filter_by(email=current_identity).first()
            if u: user_id = u.id

        if not user_id:
            return api_response(False, "User not found", status_code=404)

        # Us user ki saari chat logs database se delete karna
        ChatLog.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        app_logger.info(f"User {user_id} deleted their chat history.")
        return api_response(True, "Chat history deleted successfully")
    
    except Exception as e:
        db.session.rollback() # Agar error aaye toh changes wapas lo
        app_logger.error(f"Delete History Error: {str(e)}")
        return api_response(False, "Error deleting chat history", status_code=500)