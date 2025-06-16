"""Photo vote model for weekly photo contests."""
from datetime import datetime
from . import db


class PhotoVote(db.Model):
    """Photo vote model for tracking votes on team photos."""
    
    __tablename__ = 'photo_votes'
    
    vote_id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.photo_id'), nullable=False)
    voter_id = db.Column(db.Integer, db.ForeignKey('team_members.team_member_id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add a unique constraint to prevent multiple votes from the same voter for the same photo
    __table_args__ = (
        db.UniqueConstraint('photo_id', 'voter_id', name='unique_vote'),
    )
    
    def __repr__(self):
        return f'<PhotoVote vote_id={self.vote_id} photo_id={self.photo_id}>'
