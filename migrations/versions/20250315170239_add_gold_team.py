"""Add Gold Team with Jack and Jill

Revision ID: 20250315170239
Revises: 
Create Date: 2025-03-16 00:02:39

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = '20250315170239'
down_revision = None  # Change this if you have previous migrations
branch_labels = None
depends_on = None


def upgrade():
    # Create a reference to the teams table
    teams = table('teams',
        column('team_id', sa.Integer),
        column('team_name', sa.String),
        column('description', sa.Text),
        column('logo_url', sa.String),
        column('total_points', sa.Integer),
        column('created_at', sa.DateTime)
    )
    
    # Insert Gold Team
    op.bulk_insert(teams, [
        {
            'team_name': 'Gold Team',
            'description': 'Team consisting of Jack and Jill',
            'logo_url': '',
            'total_points': 0,
            'created_at': datetime.utcnow()
        }
    ])
    
    # Get the team_id of the inserted team
    connection = op.get_bind()
    gold_team = connection.execute(sa.select([teams.c.team_id]).where(
        teams.c.team_name == 'Gold Team'
    )).fetchone()
    gold_team_id = gold_team[0]
    
    # Create a reference to the team_members table
    team_members = table('team_members',
        column('team_member_id', sa.Integer),
        column('team_id', sa.Integer),
        column('member_name', sa.String),
        column('email', sa.String),
        column('password_hash', sa.String),
        column('is_admin', sa.Boolean),
        column('is_active', sa.Boolean)
    )
    
    # Insert team members
    op.bulk_insert(team_members, [
        {
            'team_id': gold_team_id,
            'member_name': 'Jack',
            'email': 'jack@example.com',
            'password_hash': generate_password_hash('friedrich2025'),
            'is_admin': False,
            'is_active': True
        },
        {
            'team_id': gold_team_id,
            'member_name': 'Jill',
            'email': 'jill@example.com',
            'password_hash': generate_password_hash('friedrich2025'),
            'is_admin': False,
            'is_active': True
        }
    ])


def downgrade():
    # Get the team_id for Gold Team
    connection = op.get_bind()
    teams = table('teams', column('team_id', sa.Integer), column('team_name', sa.String))
    gold_team = connection.execute(sa.select([teams.c.team_id]).where(
        teams.c.team_name == 'Gold Team'
    )).fetchone()
    
    if gold_team:
        gold_team_id = gold_team[0]
        
        # Delete team members
        team_members = table('team_members', column('team_id', sa.Integer))
        op.execute(
            team_members.delete().where(team_members.c.team_id == gold_team_id)
        )
        
        # Delete team
        op.execute(
            teams.delete().where(teams.c.team_id == gold_team_id)
        )
