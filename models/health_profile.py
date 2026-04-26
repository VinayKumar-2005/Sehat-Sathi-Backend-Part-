from extensions import db
from datetime import datetime

class HealthProfile(db.Model):
    __tablename__ = 'health_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # 1. Basic Stats
    age = db.Column(db.Integer, nullable=False, default=25)
    gender = db.Column(db.String(10), nullable=False, default="Male")
    height = db.Column(db.Float, nullable=False) # cm
    weight = db.Column(db.Float, nullable=False) # kg
    
    # 2. Medical Data
    bp = db.Column(db.String(20), default="120/80")
    sugar = db.Column(db.Float, default=90.0)
    injury = db.Column(db.String(255), default="None") # e.g. "Knee Pain"
    
    # 3. Advanced Fields (For AI Logic)
    activity_level = db.Column(db.String(50), default="Sedentary") 
    diet_preference = db.Column(db.String(20), default="Non-Veg") # Veg, Non-Veg, Vegan, Egg
    goal = db.Column(db.String(50), default="General Fitness") # Muscle Gain, Weight Loss, Powerlifting
    
    # 4. ✅ NEW: Context Awareness Fields
    workout_environment = db.Column(db.String(50), default="Gym") # Gym, Home, Yoga Studio
    experience_level = db.Column(db.String(50), default="Beginner") # Beginner, Intermediate, Advanced

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        bmi_val = 0
        if self.height and self.height > 0:
            bmi_val = round(self.weight / ((self.height/100) ** 2), 1)

        return {
            'user_id': self.user_id,
            'age': self.age,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'bp': self.bp,
            'sugar': self.sugar,
            'injury': self.injury,
            'activity_level': self.activity_level,
            'diet_preference': self.diet_preference,
            'goal': self.goal,
            'workout_environment': self.workout_environment, # ✅ Added to response
            'experience_level': self.experience_level,       # ✅ Added to response
            'bmi': bmi_val
        }