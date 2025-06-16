"""Database models."""
# Import models here to make them available when importing from the models package
from app.extensions import db
from .teams import Team
from .team_members import TeamMember
from .activities import Activity
from .team_activities import TeamActivity
from .photo import Photo
from .photo_votes import PhotoVote

__all__ = ['db', 'Team', 'TeamMember', 'Activity', 'TeamActivity', 'Photo', 'PhotoVote']
