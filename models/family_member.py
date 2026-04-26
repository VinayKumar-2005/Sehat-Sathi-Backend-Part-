from extensions import db
from datetime import datetime

class FamilyMember(db.Model):
    __tablename__ = 'family_members'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    relation = db.Column(db.String(50), nullable=False) # Father, Mother, Child, Spouse
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    
    # Medical Overview for the family member
    known_diseases = db.Column(db.String(255), default="None")
    allergies = db.Column(db.String(255), default="None")
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "relation": self.relation,
            "age": self.age,
            "gender": self.gender,
            "diseases": self.known_diseases,
            "allergies": self.allergies
        }