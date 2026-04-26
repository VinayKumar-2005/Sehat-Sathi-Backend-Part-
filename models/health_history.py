from extensions import db
from datetime import datetime

class HealthHistory(db.Model):
    __tablename__ = 'health_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # The date of this log entry
    date_logged = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    
    # Trackable Metrics
    weight = db.Column(db.Float, nullable=True)
    sugar_fasting = db.Column(db.Integer, nullable=True)
    sugar_random = db.Column(db.Integer, nullable=True)
    bp_systolic = db.Column(db.Integer, nullable=True) # Upper (120)
    bp_diastolic = db.Column(db.Integer, nullable=True) # Lower (80)
    
    # Optional Note
    note = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date_logged.strftime('%Y-%m-%d'),
            "weight": self.weight,
            "sugar": f"F:{self.sugar_fasting} R:{self.sugar_random}",
            "bp": f"{self.bp_systolic}/{self.bp_diastolic}" if self.bp_systolic else "N/A",
            "note": self.note
        }