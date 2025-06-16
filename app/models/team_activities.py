"""Team activity model for tracking participation."""
from datetime import datetime
from . import db

class TeamActivity(db.Model):
    """Team activity model for tracking team participation in activities."""
    
    __tablename__ = 'team_activities'
    
    team_activity_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    placement = db.Column(db.Integer)  # 1 for first place, 2 for second, etc.
    points_earned = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<TeamActivity team_id={self.team_id} activity_id={self.activity_id}>'
