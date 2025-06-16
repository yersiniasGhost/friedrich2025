import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from app.models import db, Photo, Team, PhotoVote
from flask_login import login_required, current_user
from sqlalchemy import func

photos_bp = Blueprint('photos', __name__)

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@photos_bp.route('/photos/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    """Handle photo uploads for the weekly contest"""

    # Get current theme from database or app config
    current_theme = "Nature"  # This should come from your database in production
    deadline = "Friday at 5:00 PM"  # Also should come from your database

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'photo' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['photo']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Create a secure version of the filename
            filename = secure_filename(file.filename)

            # Generate a unique filename using timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{filename}"

            # Get team ID from current user
            team_id = current_user.team_id  # Adjust based on your user model

            # Make sure upload directory exists
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # Save the file to the uploads folder
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)

            # Store the relative path in the database
            db_file_path = f"photos/{unique_filename}"

            # Get caption from form
            caption = request.form.get('caption', '')

            # Create database entry
            new_photo = Photo(
                file_path=db_file_path,
                caption=caption,
                uploaded_at=datetime.now(),
                team_id=team_id
            )

            db.session.add(new_photo)
            db.session.commit()

            flash('Photo successfully uploaded!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash(f'Invalid file type. Allowed file types are: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
            return redirect(request.url)

    # GET request - show the upload form
    return render_template('photos/photo_upload.html', theme=current_theme, deadline=deadline)


@photos_bp.route('/photos/gallery', methods=['GET'])
def gallery():
    """Display all photos in the current contest"""

    # Get all photos, newest first
    photos = Photo.query.order_by(Photo.uploaded_at.desc()).all()

    # Get team info for each photo
    gallery_items = []
    for photo in photos:
        team = Team.query.get(photo.team_id)
        gallery_items.append({
            'photo': photo,
            'team': team
        })

    return render_template('photos/photo_gallery.html', gallery_items=gallery_items)



@photos_bp.route('/photos/<int:photo_id>/vote', methods=['POST'])
@login_required
def vote(photo_id):
    """Handle votes for photos"""

    # Get the photo
    photo = Photo.query.get_or_404(photo_id)

    # Check if the user has already voted for this photo
    existing_vote = PhotoVote.query.filter_by(
        photo_id=photo_id,
        voter_id=current_user.team_member_id  # Adjust based on your user model
    ).first()

    if existing_vote:
        flash('You have already voted for this photo', 'error')
        return redirect(url_for('photos.gallery'))

    # Check if the user still has votes remaining for this week
    # Define the start of the current week (Monday)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())

    # Count votes cast by this user this week
    votes_this_week = PhotoVote.query.filter(
        PhotoVote.voter_id == current_user.team_member_id,  # Adjust based on your user model
        func.date(PhotoVote.voted_at) >= start_of_week
    ).count()

    # Set max votes per week
    MAX_VOTES_PER_WEEK = 3

    if votes_this_week >= MAX_VOTES_PER_WEEK:
        flash(f'You have used all your {MAX_VOTES_PER_WEEK} votes for this week', 'error')
        return redirect(url_for('photos.gallery'))

    # Create a new vote
    new_vote = PhotoVote(
        photo_id=photo_id,
        voter_id=current_user.team_member_id,  # Adjust based on your user model
        voted_at=datetime.now()
    )

    db.session.add(new_vote)
    db.session.commit()

    flash('Vote recorded successfully!', 'success')
    return redirect(url_for('photos.gallery'))


# Helper function to check if a user has voted for a specific photo
def user_has_voted_for(photo_id):
    """Check if the current user has voted for a specific photo"""
    if not current_user.is_authenticated:
        return False

    existing_vote = PhotoVote.query.filter_by(
        photo_id=photo_id,
        voter_id=current_user.team_member_id
    ).first()

    return existing_vote is not None


# Helper function to get the number of votes remaining for a user this week
def get_votes_remaining():
    """Get the number of votes remaining for the current user this week"""
    if not current_user.is_authenticated:
        return 0

    # Define the start of the current week (Monday)
    # today = datetime.now().date()
    # start_of_week = today - timedelta(days=today.weekday())

    # Count votes cast by this user this week
    votes_this_week = PhotoVote.query.filter(
        PhotoVote.voter_id == current_user.team_member_id
    ).count()

    # Set max votes per week
    MAX_VOTES_PER_WEEK = 5

    return max(0, MAX_VOTES_PER_WEEK - votes_this_week)


# Make these helper functions available to templates
@photos_bp.context_processor
def photo_helpers():
    return {
        'user_has_voted_for': user_has_voted_for,
        'votes_remaining': get_votes_remaining()
    }