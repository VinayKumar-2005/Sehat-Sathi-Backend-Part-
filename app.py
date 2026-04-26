from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt
from utils.logger import app_logger  # ✅ NEW: Logger Import

def create_app():
    app = Flask(__name__)
    
    # --- CONFIGURATION ---
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sehat_sathi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-super-secret'

    # --- INIT EXTENSIONS ---
    # Flutter Web ke liye CORS ko explicitly sabhi origins aur methods allow karne ke liye configure karein
    # CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"]}}, supports_credentials=True)
    CORS(app, origins="*", supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)

    # --- GLOBAL ERROR HANDLERS (✅ MODULE 9 SAFETY LAYER) ---
    # These ensure the app never crashes with an HTML page, always JSON
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        app_logger.error(f"Critical Server Error: {str(e)}") # Log it
        return jsonify({"success": False, "message": "Internal System Error. Engineers notified."}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app_logger.error(f"Unhandled Exception: {str(e)}")
        return jsonify({"success": False, "message": "An unexpected error occurred."}), 500

    # --- REGISTER BLUEPRINTS ---
    from routes.auth_routes import auth_bp
    from routes.profile_routes import profile_bp
    from routes.analysis import analysis_bp
    from routes.workout_routes import workout_bp
    from routes.chat_routes import chat_bp
    from routes.alert_routes import alert_bp
    from routes.progress_routes import progress_bp
    from routes.notification_routes import notification_bp

    # Ensuring consistent naming with /api prefix
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(workout_bp, url_prefix='/api/workout')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(alert_bp, url_prefix='/api/alerts')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')

    # --- CREATE TABLES ---
    with app.app_context():
        # Import all models here so SQLAlchemy knows about them
        from models.user import User
        from models.health_profile import HealthProfile
        from models.health_history import HealthHistory
        from models.family_member import FamilyMember
        from models.workout_log import WorkoutLog 
        from models.workout_plan import WorkoutPlan 
        from models.chat_log import ChatLog
        from models.health_alert import HealthAlert
        from models.reminder import Reminder
        
        db.create_all()

    return app

# Global App Instance
app = create_app()

if __name__ == '__main__':
    app_logger.info("SehatSaathi Backend Starting...") 
    app.run(host='0.0.0.0', port=5000, debug=True) # 🟢 ADDED: host='0.0.0.0'