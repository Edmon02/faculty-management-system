# app/models/user.py
from datetime import datetime
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model):
    """User account model"""

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    _id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False, default="student")
    failed_attempts = db.Column(db.Integer, default=0)
    last_failed_attempt = db.Column(db.DateTime)

    def __init__(self, username: str, password: str, _id: int, user_type: str = "student"):
        self.username = username
        self.password = generate_password_hash(password)
        self._id = _id
        self.type = user_type

    def check_password(self, password: str) -> bool:
        """Verify the password against its hash"""
        return check_password_hash(self.password, password)

    def is_blocked(self) -> bool:
        """Check if user is blocked due to too many failed attempts"""
        if self.failed_attempts >= 3 and self.last_failed_attempt:
            block_time = self.last_failed_attempt.timestamp() + 1800  # 30 minutes
            current_time = datetime.now().timestamp()
            return current_time < block_time
        return False

    def reset_failed_attempts(self) -> None:
        """Reset failed login attempts counter"""
        self.failed_attempts = 0
        db.session.commit()

    def increment_failed_attempt(self) -> None:
        """Increment failed attempt counter and update timestamp"""
        self.failed_attempts += 1
        self.last_failed_attempt = datetime.now()
        db.session.commit()

    def __repr__(self) -> str:
        return f"<User {self.username}>"
