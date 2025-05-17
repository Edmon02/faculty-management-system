# app/models/subject.py
from typing import Any, Dict, List

from app import db


class Subject(db.Model):
    """Subject model"""

    __tablename__ = "Subject"

    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)
    group_name = db.Column(db.String(50))
    messenge = db.Column(db.Text)

    # Relationships
    files = db.relationship("Files", secondary="SubjectFile", backref="subjects")

    def to_dict(self) -> Dict[str, Any]:
        """Convert subject data to dictionary"""
        return {
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "group_name": self.group_name,
            "messenge": self.messenge,
            "files": [file.to_dict(include_data=False) for file in self.files],
        }

    def __repr__(self) -> str:
        return f"<Subject {self.subject_name}>"


class Files(db.Model):
    """File storage model"""

    __tablename__ = "Files"

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.LargeBinary, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)

    def to_dict(self, include_data: bool = False) -> Dict[str, Any]:
        """Convert file data to dictionary"""
        import os

        result = {"id": self.id, "file_name": self.file_name, "file_type": os.path.splitext(self.file_name)[1]}

        if include_data:
            import base64

            result["file_data"] = base64.b64encode(self.file).decode("utf-8")

        return result

    def __repr__(self) -> str:
        return f"<File {self.file_name}>"


class SubjectFile(db.Model):
    """Association table between subjects and files"""

    __tablename__ = "SubjectFile"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subject.subject_id"), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey("Files.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<SubjectFile {self.subject_id}-{self.file_id}>"


class SubjectLecturerGroup(db.Model):
    """Association table for subjects, lecturers and groups"""

    __tablename__ = "SubjectLecturerGroup"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subject.subject_id"), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("Lecturer.id"), nullable=False)
    group_name = db.Column(db.String(50), nullable=False)

    # Relationships
    subject = db.relationship("Subject", backref="lecturer_groups")
    lecturer = db.relationship("Lecturer", backref="subject_groups")

    def __repr__(self) -> str:
        return f"<SubjectLecturerGroup {self.subject_id}-{self.lecturer_id}-{self.group_name}>"
