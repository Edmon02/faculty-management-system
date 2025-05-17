# app/controllers/auth_controller.py
from datetime import datetime, timedelta

from flask import session

from app.services.auth_service import AuthService

# from app.utils.security import get_mac_address


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def authenticate(self, username, password, remote_addr):
        # Check if the user is blocked due to consecutive failed attempts
        user_status = self.auth_service.check_user_status(username)

        if user_status.get("blocked", False):
            return {"message": "User is blocked. Try again later."}, 403

        # Attempt to authenticate the user
        user_data = self.auth_service.authenticate_user(username, password)

        if not user_data:
            # Increment failed attempts
            self.auth_service.increment_failed_attempts(username)
            return {"message": "Incorrect username or password"}, 500

        # Get user details based on user type
        data = self.auth_service.get_user_details(user_data)

        if not data:
            return {"message": "User details not found"}, 500

        # Get group IDs for the user
        group_ids = self.auth_service.get_user_groups(user_data, data)

        # Reset failed login attempts
        self.auth_service.reset_failed_attempts(username)

        # Log user activity
        self.auth_service.log_user_activity()

        # Set up the user session
        current_ip = remote_addr

        session.update(
            {
                "logged_in": True,
                "type": user_data["type"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "is_Admin": data.get("is_Admin", 0),
                "is_Lecturer": data.get("is_Lecturer", 0),
                "ID": data["id"],
                "user_ip": current_ip,
                "group_ids": group_ids if isinstance(group_ids, list) else (group_ids,),
            }
        )

        return {"message": "Login successful"}, 200
