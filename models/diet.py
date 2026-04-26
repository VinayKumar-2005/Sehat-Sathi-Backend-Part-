from database.db import db

class Diet(db.Model):
    __tablename__ = 'diet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    
    is_veg = db.Column(db.Boolean, default=True)
    is_sugar_free = db.Column(db.Boolean, default=False)
    restricted_for = db.Column(db.String(255), nullable=True) # e.g. "Diabetes, BP"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,
            'is_veg': self.is_veg,
            'is_sugar_free': self.is_sugar_free,
            'restricted_for': self.restricted_for
        }