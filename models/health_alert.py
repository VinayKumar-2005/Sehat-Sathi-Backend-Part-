from extensions import db
from datetime import datetime

class HealthAlert(db.Model):
    __tablename__ = 'health_alerts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Levels: LOW, MEDIUM, HIGH, CRITICAL
    severity = db.Column(db.String(20), nullable=False)
    
    # Type: "High BP", "Low Sugar", "Arrhythmia Risk", etc.
    alert_type = db.Column(db.String(50), nullable=False)
    
    # Message: "Your BP is 180/110. Seek immediate help."
    message = db.Column(db.Text, nullable=False)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'severity': self.severity,
            'alert_type': self.alert_type,
            'message': self.message,
            'timestamp': self.created_at.isoformat()
        }