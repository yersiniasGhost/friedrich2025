"""
Team Activity Web Application
----------------------------
A web application for managing team activities, leaderboards, and photo contests.
"""

from flask import Flask, send_from_directory
from datetime import datetime


def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = False

    # Load config based on config_name
    from config import config_by_name
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    from app.extensions import db, migrate, login_manager, mail, csrf
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.controllers.main import main
    from app.controllers.auth import auth
    from app.controllers.activities import activities
    from app.controllers.photo_bp import photos_bp
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(activities)
    app.register_blueprint(photos_bp)

    # Add current datetime to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}


    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app