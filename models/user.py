from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    # Relationships
    profile = db.relationship('HealthProfile', backref='user', uselist=False, cascade="all, delete")
    history = db.relationship('HealthHistory', backref='user', lazy=True, cascade="all, delete")
    family_members = db.relationship('FamilyMember', backref='user', lazy=True, cascade="all, delete") # ✅ Added Family Link

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return { "id": self.id, "username": self.username, "email": self.email }