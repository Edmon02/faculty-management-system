# app/models/__init__.py
from datetime import datetime

from app import db
from app.models.activity import ActivityLog
from app.models.exercise import Exercise, ExerciseGroup, WaitRoom
from app.models.lecturer import Lecturer
from app.models.news import AudioChunk, News
from app.models.student import Student
from app.models.subject import Files, Subject, SubjectFile
from app.models.thesis import Thesis

# Import all models to make them available when importing from models
from app.models.user import User
