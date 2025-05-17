import os
import re
from datetime import datetime


def validate_username(username):
    """Validate that a username meets requirements."""
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"
    return True, "Valid username"


def validate_password(password):
    """Validate that a password meets security requirements."""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, "Valid password"


def validate_email(email):
    """Validate that a string is a properly formatted email address."""
    if not email:
        return False, "Email cannot be empty"

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, "Valid email"


def validate_phone_number(phone):
    """Validate that a string is a properly formatted phone number."""
    if not phone:
        return False, "Phone number cannot be empty"

    # Remove common phone number formatting characters
    cleaned_phone = re.sub(r"[\s\-\(\)\.]", "", phone)

    # Check if the remaining string consists of only digits and is of reasonable length
    if not cleaned_phone.isdigit() or len(cleaned_phone) < 8:
        return False, "Invalid phone number format"

    return True, "Valid phone number"


def validate_date(date_str, format_str="%Y-%m-%d"):
    """Validate that a string is a properly formatted date."""
    if not date_str:
        return False, "Date cannot be empty"

    try:
        datetime.strptime(date_str, format_str)
        return True, "Valid date"
    except ValueError:
        return False, f"Invalid date format. Expected format: {format_str}"


def validate_file_extension(filename, allowed_extensions):
    """Validate that a file has an allowed extension."""
    if not filename:
        return False, "No file selected"

    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext not in allowed_extensions:
        return False, f"File extension not allowed. Allowed extensions: {', '.join(allowed_extensions)}"

    return True, "Valid file extension"


def validate_file_size(file, max_size_mb=5):
    """Validate that a file is not too large."""
    if not file:
        return False, "No file provided"

    # Get the file size in bytes
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file position

    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        return False, f"File too large. Maximum size: {max_size_mb}MB"

    return True, "Valid file size"


def validate_required_fields(data, required_fields):
    """Validate that all required fields are present and non-empty."""
    missing_fields = []

    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    return True, "All required fields provided"
