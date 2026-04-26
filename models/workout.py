from database.db import db

class Workout(db.Model): 
    __tablename__ = 'workouts' # Standard naming convention (plural)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # ✅ Fields required by seed_data.py
    workout_type = db.Column(db.String(100), nullable=False)  # Renamed from 'type' to fix reserved keyword issue
    calories_burn_per_hr = db.Column(db.Integer, nullable=False) # Maps to 'burn' in seed data
    unsafe_for = db.Column(db.String(255), default="None")

    # ✅ New Fields you added (Set to Nullable=True so seeding doesn't crash)
    duration_minutes = db.Column(db.Integer, default=30)
    difficulty = db.Column(db.String(50), nullable=True) # Made optional for now
    target_muscle = db.Column(db.String(100), nullable=True) # Made optional for now

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'workout_type': self.workout_type,
            'calories_burn_per_hr': self.calories_burn_per_hr,
            'unsafe_for': self.unsafe_for,
            'duration_minutes': self.duration_minutes,
            'difficulty': self.difficulty,
            'target_muscle': self.target_muscle
        }


    def __repr__(self):
        return f"<Workout {self.name}>"