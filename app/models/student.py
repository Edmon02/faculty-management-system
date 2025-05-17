# app/models/student.py
from datetime import datetime
from typing import List, Optional

from app import db


class Student(db.Model):
    """Student model"""

    __tablename__ = "Student"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    birthday_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    image = db.Column(db.LargeBinary)
    rating = db.Column(db.Integer, default=0)
    address = db.Column(db.String(200))

    # Relationships
    user = db.relationship("User", backref="student", primaryjoin="Student.id == User._id", foreign_keys="User._id", uselist=False)
    thesis = db.relationship("Thesis", backref="student", uselist=False)
    wait_rooms = db.relationship("WaitRoom", backref="student", lazy="dynamic")

    def to_dict(self) -> dict:
        """Convert student data to dictionary"""
        return {
            "id": self.id,
            "group_name": self.group_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "patronymic": self.patronymic,
            "birthday_date": self.birthday_date.strftime("%Y-%m-%d") if self.birthday_date else None,
            "phone": self.phone,
            "rating": self.rating,
            "address": self.address,
        }

    def __repr__(self) -> str:
        return f"<Student {self.first_name} {self.last_name}>"
