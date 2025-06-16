"""Activity model."""
from datetime import datetime
from . import db

class Activity(db.Model):
    """Activity model for team events and challenges."""
    
    __tablename__ = 'activities'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    scheduled_at = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    location = db.Column(db.String(255))
    rules = db.Column(db.Text)
    participation_points = db.Column(db.Integer, default=0)
    first_place_points = db.Column(db.Integer, default=0)
    second_place_points = db.Column(db.Integer, default=0)
    third_place_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team_activities = db.relationship('TeamActivity', backref='activity', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Activity {self.name}>'
