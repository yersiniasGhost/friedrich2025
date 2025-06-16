"""Team member model."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class TeamMember(UserMixin, db.Model):
    """Team member model for individuals in teams."""
    
    __tablename__ = 'team_members'
    
    team_member_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    member_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def get_id(self):
        """Return the unique identifier for Flask-Login."""
        return str(self.team_member_id)
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<TeamMember {self.member_name}>'
