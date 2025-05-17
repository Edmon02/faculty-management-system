# app/models/lecturer.py
from typing import Any, Dict, List

from app import db

lecturer_group = db.Table("LecturerGroup", db.Column("lecturer_id", db.Integer, db.ForeignKey("Lecturer.id")), db.Column("group_name", db.String(50)))


class Lecturer(db.Model):
    """Lecturer model"""

    __tablename__ = "Lecturer"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    academic_degree = db.Column(db.String(50))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    images = db.Column(db.LargeBinary)
    is_Admin = db.Column(db.Boolean, default=False)
    is_Lecturer = db.Column(db.Boolean, default=True)

    # Relationships
    groups = db.relationship("Group", secondary=lecturer_group, backref="lecturers")
    user = db.relationship("User", backref="lecturer", primaryjoin="Lecturer.id == User._id", foreign_keys="User._id", uselist=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert lecturer data to dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "academic_degree": self.academic_degree,
            "position": self.position,
            "email": self.email,
            "phone": self.phone,
            "is_Admin": self.is_Admin,
            "is_Lecturer": self.is_Lecturer,
        }

    def __repr__(self) -> str:
        return f"<Lecturer {self.first_name} {self.last_name}>"


class Group(db.Model):
    """Group model for organizing students"""

    __tablename__ = "Group"

    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(200))

    # Relationships
    students = db.relationship("Student", backref="group", primaryjoin="Group.name == Student.group_name", foreign_keys="Student.group_name")
