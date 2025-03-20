"""Activities routes."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.activities import Activity
from app.models.team_activities import TeamActivity
from app.models.teams import Team
from datetime import datetime

activities = Blueprint('activities', __name__)


@activities.route('/activities')
@login_required
def index():
    """Activities dashboard."""
    # Get all activities
    all_activities = Activity.query.order_by(Activity.scheduled_at).all()

    # Get the team's participation in activities
    team = Team.query.get(current_user.team_id)
    team_activities = TeamActivity.query.filter_by(team_id=current_user.team_id).all()

    # Create a dictionary of team participation for easy lookup
    participation = {}
    for team_activity in team_activities:
        participation[team_activity.activity_id] = team_activity

    return render_template('activities/index.html',
                           activities=all_activities,
                           participation=participation,
                           team=team)


@activities.route('/activities/<int:activity_id>')
@login_required
def show(activity_id):
    """Show a single activity."""
    activity = Activity.query.get_or_404(activity_id)
    team_activity = TeamActivity.query.filter_by(
        team_id=current_user.team_id,
        activity_id=activity_id
    ).first()

    return render_template('activities/show.html',
                           activity=activity,
                           team_activity=team_activity)


@activities.route('/activities/<int:activity_id>/participate', methods=['POST'])
@login_required
def participate(activity_id):
    """Record participation in an activity."""
    activity = Activity.query.get_or_404(activity_id)

    # Check if team has already participated
    existing = TeamActivity.query.filter_by(
        team_id=current_user.team_id,
        activity_id=activity_id
    ).first()

    if existing:
        flash('Your team has already recorded participation in this activity.', 'info')
        return redirect(url_for('activities.show', activity_id=activity_id))

    # Record participation
    placement = request.form.get('placement', type=int)

    # Calculate points based on placement
    points_earned = activity.participation_points
    if placement == 1:
        points_earned += activity.first_place_points
    elif placement == 2:
        points_earned += activity.second_place_points
    elif placement == 3:
        points_earned += activity.third_place_points

    # Create team activity record
    team_activity = TeamActivity(
        team_id=current_user.team_id,
        activity_id=activity_id,
        completed_at=datetime.utcnow(),
        placement=placement,
        points_earned=points_earned,
        verified=False  # Admin needs to verify
    )
    db.session.add(team_activity)

    # Update team total points (but don't commit yet)
    team = Team.query.get(current_user.team_id)
    team.total_points += points_earned

    db.session.commit()

    flash(f'Participation recorded! You earned {points_earned} points.', 'success')
    return redirect(url_for('activities.show', activity_id=activity_id))
