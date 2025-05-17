# app/models/activity.py
from datetime import datetime

from app import db


class ActivityLog(db.Model):
    """Activity log for tracking user activity"""

    __tablename__ = "ActivityLog"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM
    activity_count = db.Column(db.Integer, default=1)

    @classmethod
    def log_activity(cls, date_str=None):
        """Log activity for current month or specified date"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m")

        activity = cls.query.filter_by(date=date_str).first()
        if activity:
            activity.activity_count += 1
        else:
            activity = cls(date=date_str)
            db.session.add(activity)

        db.session.commit()
        return activity

    def __repr__(self) -> str:
        return f"<ActivityLog {self.date}: {self.activity_count}>"


# Archived tables for tracking changes
class ArchiveStudent(db.Model):
    """Archive of student changes"""

    __tablename__ = "Archive_student"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    birthday_date = db.Column(db.Date)
    group_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    archived_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"<ArchiveStudent {self.student_id}>"


class ArchiveTeacher(db.Model):
    """Archive of teacher changes"""

    __tablename__ = "Archive_teacher"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    academic_degree = db.Column(db.String(50))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100))
    images = db.Column(db.LargeBinary)
    is_Admin = db.Column(db.Boolean, default=False)
    is_Lecturer = db.Column(db.Boolean, default=True)
    archived_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"<ArchiveTeacher {self.teacher_id}>"
