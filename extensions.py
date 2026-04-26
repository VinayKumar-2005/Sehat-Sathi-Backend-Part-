from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize extensions here (detached from app)
db = SQLAlchemy()
jwt = JWTManager()