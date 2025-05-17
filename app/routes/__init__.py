# app/routes/__init__.py
from flask import Blueprint

# Import all route blueprints
from app.routes.auth import auth_bp
from app.routes.chatbot import chatbot_bp
from app.routes.dashboard import dashboard_bp
from app.routes.exercises import exercises_bp
from app.routes.news import news_bp
from app.routes.students import students_bp
from app.routes.subjects import subjects_bp
from app.routes.teachers import teachers_bp


# Function to register all blueprints
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(chatbot_bp)
