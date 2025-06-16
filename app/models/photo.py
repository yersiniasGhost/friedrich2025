"""Photo model for weekly contests."""
from datetime import datetime
from . import db

class Photo(db.Model):
    """Photo model for team photo submissions."""
    
    __tablename__ = 'photos'
    
    photo_id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    contest_week = db.Column(db.String(20))  # Format: YYYY-WW
    
    # Relationships
    votes = db.relationship('PhotoVote', backref='photo', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Photo {self.photo_id} by team_id={self.team_id}>'
