from extensions import db
from datetime import datetime

class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 👇 YAHAN CHANGE KIYA HAI ('user.id' -> 'users.id')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    
    exercise_name = db.Column(db.String(100), nullable=False)
    sets_done = db.Column(db.Integer, nullable=False)
    reps_done = db.Column(db.Integer, nullable=False)
    weight_kg = db.Column(db.Float, nullable=True)
    
    notes = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime('%Y-%m-%d'),
            "exercise": self.exercise_name,
            "sets": self.sets_done,
            "reps": self.reps_done,
            "weight": self.weight_kg,
            "notes": self.notes
        }