# app/services/auth_service.py
import hashlib
import random
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.user import User


class AuthService:
    @staticmethod
    def random_numbers(length: int) -> str:
        """Generate a random string of numbers."""
        return "".join(str(random.randint(0, 9)) for _ in range(length))

    @staticmethod
    def random_password(length: int) -> str:
        """Generate a random password of specified length."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_user_credentials(username: str, password: str) -> Tuple[bool, Optional[Dict], Optional[Dict]]:
        """
        Check user credentials and return user data if valid.

        Args:
            username: The username to check
            password: The password to check

        Returns:
            Tuple containing:
            - Boolean indicating if credentials are valid
            - User data dictionary if valid, None otherwise
            - Related entity data (Student or Lecturer) if valid, None otherwise
        """
        # First check if the user is blocked due to too many failed attempts
        user = User.query.filter_by(username=username).first()

        if not user:
            return False, None, None

        if user.failed_attempts and user.last_failed_attempt:
            if user.failed_attempts >= 3 and datetime.strptime(user.last_failed_attempt, "%Y-%m-%d %H:%M:%S.%f") + timedelta(minutes=30) > datetime.now():
                return False, None, None

        # Check if credentials are valid
        user_record = User.query.filter_by(username=username, password=password).first()

        if not user_record:
            # Increment failed attempts
            if user:
                user.failed_attempts = (user.failed_attempts or 0) + 1
                user.last_failed_attempt = datetime.now()
                user.save()
            return False, None, None

        # Reset failed attempts on successful login
        user_record.failed_attempts = 0
        user_record.save()

        user_data = user_record.to_dict()

        # Get related entity data based on user type
        entity_data = None
        if user_data["type"] == "student":
            entity = Student.query.filter_by(id=user_data["_id"]).first()
        else:
            entity = Lecturer.query.filter_by(id=user_data["_id"]).first()

        if entity:
            entity_data = entity.to_dict()

        return True, user_data, entity_data
