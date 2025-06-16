"""Team model."""
from datetime import datetime
from . import db

class Team(db.Model):
    """Team model representing a 2-person team."""
    
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    total_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('TeamActivity', backref='team', lazy='dynamic', cascade='all, delete-orphan')
    photos = db.relationship('Photo', backref='team', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Team {self.team_name}>'
