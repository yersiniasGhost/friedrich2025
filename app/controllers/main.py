"""Main routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.controllers.auth import admin_required
from app.models.teams import Team
from app.models.photo import Photo
from app.models.photo_votes import PhotoVote
from app.controllers.photo_bp import user_has_voted_for, get_votes_remaining


main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page."""
    # If user is not authenticated, show splash page
    if not current_user.is_authenticated:
        return render_template('main/splash.html')
    # Otherwise show the regular home page
    return render_template('main/index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    # Get the team data for the current user
    team = Team.query.get(current_user.team_id)
    # return render_template('main/dashboard.html', team=team)


    recent_photos = Photo.query.order_by(Photo.uploaded_at.desc()).limit(5).all()

    # Import the helper functions from the photos blueprint

    # Get vote counts for each photo
    photo_vote_counts = {}
    for photo in recent_photos:
        photo_vote_counts[photo.photo_id] = PhotoVote.query.filter_by(photo_id=photo.photo_id).count()

    return render_template(
        'main/dashboard.html',
        recent_photos=recent_photos,
        photo_vote_counts=photo_vote_counts,
        user_has_voted_for=user_has_voted_for,
        votes_remaining=get_votes_remaining(),
        team=team
    )


@main.route('/calendar')
@login_required
def calendar():
    """Calendar page."""
    return render_template('main/calendar.html')

@main.route('/leaderboard')
@login_required
def leaderboard():
    """Leaderboard page."""
    return render_template('main/leaderboard.html')

@main.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard."""
    return render_template('main/admin_dashboard.html')
