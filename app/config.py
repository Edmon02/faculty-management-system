# app/config.py
import os
import secrets
from datetime import timedelta
from pathlib import Path

basedir = Path(__file__).parent.parent.absolute()


class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(16))
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CUSTOM_404_PAGE = ("404.html", 404)
    CUSTOM_429_PAGE = ("404.html", 429)
    # RATELIMIT_STORAGE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'rate_limits.sqlite')}"
    RATELIMIT_STRATEGY = "fixed-window"  # Best for SQLite
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_DEFAULT = ["200 per day", "50 per hour"]  # Global defaults
    RATELIMIT_STORAGE_OPTIONS = {"connect_args": {"check_same_thread": False}, "poolclass": "StaticPool"}

    # Restricted routes configuration
    RESTRICTED_ROUTES = {
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

    # Rate limits for specific routes (customize as needed)
    RATELIMIT_ROUTES = {"/auth/login": ["10 per minute"], "/auth/register": ["5 per hour"], "/api/": ["100 per hour"], "/admin/": ["30 per minute"]}

    # Admin MAC address
    ADMIN_MAC_ADDRESS = "36:da:68:a3:8c:32"


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app", "pulpit.sqlite")}'
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    # Disable rate limiting in tests or use memory
    RATELIMIT_STORAGE_URI = "memory://"


class ProductionConfig(Config):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f'sqlite:///{os.path.join(basedir, "app", "pulpit.sqlite")}'


config = {"development": DevelopmentConfig, "testing": TestingConfig, "production": ProductionConfig, "default": DevelopmentConfig}
