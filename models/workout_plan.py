from extensions import db
from datetime import datetime
import json

class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Hum pura AI output JSON format mein text bankar save karenge
    plan_data = db.Column(db.Text, nullable=False) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'plan': json.loads(self.plan_data), # Text wapas JSON ban jayega
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }