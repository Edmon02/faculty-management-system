import hashlib
import random
import secrets
import string
import uuid
from functools import wraps

from flask import flash, redirect, render_template, session, url_for


def get_mac_address():
    """Get the MAC address of the current machine."""
    mac_address = ":".join(["{:02x}".format((uuid.getnode() >> elements) & 0xFF) for elements in range(0, 2 * 6, 2)][::-1])
    return mac_address


def random_numbers(length):
    """Generate a random string of numbers of specified length."""
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def random_password(length):
    """Generate a random password of specified length."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_secret_key():
    """Generate a secure secret key for Flask application."""
    return secrets.token_hex(16)


def check_restricted_route():
    """Check if the current route is restricted for the user type."""
    # Dictionary of restricted routes for each user type
    restricted_routes = {
        "student": [
            "/students/add-student",
            "/students/edit-student",
            "/add-teacher",
            "/edit-teacher",
            "/waitingroom",
            "/add-news",
            "/exercise",
            "/add-exercise",
            "/edit-exercise",
        ],
        "lecturer": [
            "/students/add-student",
            "/students/edit-student",
            "/add-teacher",
            "/edit-teacher",
            "/add-news",
        ],
        "admin": [],
    }

    from flask import request

    requested_path = request.path
    user_type = session.get("type")

    # Check if the user is accessing a restricted path
    if user_type and requested_path in restricted_routes.get(user_type, []):
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("auth.login"))  # Redirect to login page
    return None


def login_required(f):
    """Decorator to require login for routes."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorator to require admin privileges for routes."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or session.get("type") != "admin":
            return render_template("404.html"), 404
        return f(*args, **kwargs)

    return decorated_function


def lecturer_required(f):
    """Decorator to require lecturer privileges for routes."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or session.get("type") not in ["admin", "lecturer"]:
            return render_template("404.html"), 404
        return f(*args, **kwargs)

    return decorated_function
