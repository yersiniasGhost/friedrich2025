from app import create_app
from app.models import db, Team, TeamMember
from werkzeug.security import generate_password_hash

def create_gold_team():
    """Create Gold Team with Jack and Jill"""
    app = create_app()
    with app.app_context():
        # Create a new team
        gold_team = Team(
            team_name="Gold Team",
            description="Team consisting of Jack and Jill",
            logo_url="",
            total_points=0
        )
        
        # Add team to database
        db.session.add(gold_team)
        db.session.commit()
        
        # Now create team members
        jack = TeamMember(
            team_id=gold_team.team_id,
            member_name="Jack",
            email="jack@example.com",
            password_hash=generate_password_hash("friedrich2025"),
            is_admin=False,
            is_active=True
        )
        
        jill = TeamMember(
            team_id=gold_team.team_id,
            member_name="Jill",
            email="jill@example.com",
            password_hash=generate_password_hash("friedrich2025"),
            is_admin=False,
            is_active=True
        )
        
        # Add members to database
        db.session.add(jack)
        db.session.add(jill)
        db.session.commit()
        
        print(f"Created Gold Team (ID: {gold_team.team_id}) with members Jack and Jill")
        print(f"Login credentials:")
        print(f"Jack: email=jack@example.com, password=friedrich2025")
        print(f"Jill: email=jill@example.com, password=friedrich2025")

if __name__ == '__main__':
    create_gold_team()
