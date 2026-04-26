from extensions import db
from datetime import datetime

class ChatLog(db.Model):
    __tablename__ = 'chat_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # "user" or "ai"
    sender = db.Column(db.String(10), nullable=False) 
    
    # The actual text content
    message = db.Column(db.Text, nullable=False)
    
    # Context snapshot (Optional: Store what the user's goal was at this time)
    context_snapshot = db.Column(db.String(100), nullable=True)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sender': self.sender,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }