"""Authentication routes."""
from functools import wraps
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.team_members import TeamMember
from app.models.teams import Team
from app.forms.auth import LoginForm
from app.extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        member = TeamMember.query.filter_by(email=form.email.data.lower()).first()
        # For this application, we'll use a shared password
        # In a production app, you'd check the actual password
        if member is not None and form.password.data == 'friedrich2025':
            login_user(member, form.remember_me.data)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            return redirect(next_page)
        flash('Invalid email or password.')
    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

# Admin access decorator - for use in other routes
def admin_required(f):
    """Decorator for routes that require admin access."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need admin privileges to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
