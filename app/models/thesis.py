# app/models/thesis.py
from app import db


class Thesis(db.Model):
    """Thesis model"""

    __tablename__ = "Thesis"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("Student.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Thesis {self.title}>"
