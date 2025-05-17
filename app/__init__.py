# app/__init__.py
import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData

from app.config import config

# Initialize extensions
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10000 per day", "1000 per hour"],
)


def create_app(config_name=None):
    """Application factory function to create and configure the Flask app"""
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    # CORS(app, origins=["http://localhost:3000/"])

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.exercises import exercises_bp
    from app.routes.news import news_bp
    from app.routes.students import students_bp
    from app.routes.subjects import subjects_bp
    from app.routes.teachers import teachers_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(chatbot_bp)

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return app.config["CUSTOM_404_PAGE"]

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return app.config["CUSTOM_429_PAGE"]

    # Register before_request handler
    @app.before_request
    def check_user_access():
        from app.utils.security import check_restricted_route

        return check_restricted_route()

    # Serve React app for non-API routes
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react_app(path):
        # If the path starts with /api, let the blueprints handle it
        if path.startswith("api"):
            return jsonify({"error": "API route not found"}), 404
        # Otherwise, serve the React app
        return send_from_directory(app.template_folder, "index.html")

    # Initialize database if needed
    with app.app_context():
        db.create_all()

    return app
