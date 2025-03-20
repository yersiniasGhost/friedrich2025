from app import create_app
from app.models import db, Activity
from datetime import datetime, timedelta

app = create_app('development')
with app.app_context():
    # Create sample activities
    activities = [
        {
            'name': 'Washoo Tournament',
            'description': 'Join our traditional Friedrich Washoo Tournament. Teams will play in an elimination round style tournament.',
            'category': 'Games',
            'scheduled_at': datetime.utcnow() + timedelta(days=5),
            'duration_minutes': 180,
            'location': 'Home',
            'rules': 'Standard Washoo rules apply. Teams must have 2 players.',
            'participation_points': 50,
            'first_place_points': 150,
            'second_place_points': 100,
            'third_place_points': 75
        },
        {
            'name': 'Whiskey Trivia Night',
            'description': 'Test your knowledge with our trivia night. Categories include history, geography, science, and pop culture.',
            'category': 'Knowledge',
            'scheduled_at': datetime.utcnow() + timedelta(days=8),
            'duration_minutes': 120,
            'location': 'Event Hall',
            'rules': 'No phones or electronic devices allowed. Teams will answer 50 questions across 5 rounds.',
            'participation_points': 40,
            'first_place_points': 120,
            'second_place_points': 80,
            'third_place_points': 60
        },
        {
            'name': 'Hiking Challenge',
            'description': 'Navigate the Oregon trails and complete checkpoints along the way. Participation wins!',
            'category': 'Outdoor',
            'scheduled_at': datetime.utcnow() + timedelta(days=12),
            'duration_minutes': 240,
            'location': 'Mountain Trail',
            'rules': 'Teams must stay together at all times. All checkpoints must be completed in order.',
            'participation_points': 60,
            'first_place_points': 160,
            'second_place_points': 120,
            'third_place_points': 90
        },
        {
            'name': 'Photo Scavenger Hunt',
            'description': 'Find and photograph items from the scavenger hunt list. Creativity counts!',
            'category': 'Creative',
            'scheduled_at': datetime.utcnow() + timedelta(days=15),
            'duration_minutes': 150,
            'location': 'Town Center',
            'rules': 'Photos must be taken during the event time. All team members must appear in at least one photo.',
            'participation_points': 45,
            'first_place_points': 130,
            'second_place_points': 90,
            'third_place_points': 70
        },
        {
            'name': 'Cooking and Cleaning',
            'description': "Prepare a signature dish using your own mystery ingredients.   Help clean up someone's mess",
            'category': 'Home',
            'scheduled_at': datetime.utcnow() + timedelta(days=18),
            'duration_minutes': 120,
            'location': 'Community Kitchen',
            'rules': 'All ingredients must be used. Teams have 90 minutes to prepare and plate their dish.',
            'participation_points': 55,
            'first_place_points': 140,
            'second_place_points': 95,
            'third_place_points': 75
        }
    ]

    # Add activities to database
    for activity_data in activities:
        activity = Activity(**activity_data)
        db.session.add(activity)

    # Commit to database
    db.session.commit()

    print(f"Created {len(activities)} sample activities")
