from extensions import db
from datetime import datetime

class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Title: "Drink Water", "Take Vit C", "Gym Time"
    title = db.Column(db.String(100), nullable=False)
    
    # Time: "08:00", "20:30" (24-hour format string)
    time_str = db.Column(db.String(5), nullable=False)
    
    # Type: "med", "workout", "water", "custom"
    type = db.Column(db.String(20), default="custom")
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "time": self.time_str,
            "type": self.type,
            "active": self.is_active
        }