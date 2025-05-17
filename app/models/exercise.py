# app/models/exercise.py
from datetime import datetime
from typing import Any, Dict

from app import db


class Exercise(db.Model):
    """Exercise model"""

    __tablename__ = "Exercises"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50))
    expiry_time = db.Column(db.Date, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    messenge = db.Column(db.Text)
    file_name = db.Column(db.String(255))
    checkkType = db.Column(db.Integer, default=0)

    # Relationships
    groups = db.relationship("ExerciseGroup", backref="exercise", lazy="dynamic")
    wait_rooms = db.relationship("WaitRoom", backref="exercise", lazy="dynamic")

    def to_dict(self) -> Dict[str, Any]:
        """Convert exercise data to dictionary"""
        import os

        return {
            "id": self.id,
            "group_name": self.group_name,
            "expiry_time": self.expiry_time.strftime("%Y-%m-%d"),
            "subject_name": self.subject_name,
            "messenge": self.messenge,
            "file_name": self.file_name,
            "file_type": os.path.splitext(self.file_name)[1] if self.file_name else None,
            "checkkType": self.checkkType,
        }

    def __repr__(self) -> str:
        return f"<Exercise {self.id}>"


class ExerciseGroup(db.Model):
    """Association table between exercises and groups"""

    __tablename__ = "ExercisesGroup"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("Exercises.id"), nullable=False)
    group_name = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<ExerciseGroup {self.exercise_id}-{self.group_name}>"


class WaitRoom(db.Model):
    """Wait room for exercises submission tracking"""

    __tablename__ = "WaitRoom"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("Student.id"), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("Exercises.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<WaitRoom {self.student_id}-{self.exercise_id}>"
