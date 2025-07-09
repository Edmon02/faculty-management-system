# 5. Configuration & Customization: Tuning Your FMS Engine 🛠️

Welcome to the FMS control room! Proper configuration is the secret sauce that allows the Faculty Management System to adapt seamlessly to different environments – whether it's your local development playground, a staging area for testing, or the bright lights of a live production server. It also provides pathways to customize some of its core behaviors. Let's pop the hood and see how it's done.

## The `.env` File: Your Local Settings Dashboard 📝

Think of the `.env` file as a personal sticky note for your FMS application, living in the project's root directory. It's where you can jot down settings specific to *your* local setup without changing the main codebase. And because it might contain sensitive information (like secret keys or database passwords), it's a golden rule to **add `.env` to your `.gitignore` file** – we don't want those secrets accidentally wandering into our shared code repository!

While FMS can often start up with sensible defaults (especially for development using SQLite, thanks to `app/config.py`), using a `.env` file is best practice for overriding these defaults or for settings you don't want in version control.

**A Typical `.env` File Might Look Like This:**

```env
# Flask Specific - Tells Flask how to find and run your app
FLASK_APP=run.py
FLASK_CONFIG=development  # Set to 'production' or 'testing' for other environments

# Application Security - CRITICAL!
# This key is used for signing sessions and other security bits.
# Make it long, random, and keep it secret!
SECRET_KEY='your_very_long_random_and_ultra_secret_key_goes_here_do_not_share!'

# Database Configuration (more relevant for production or custom dev setups)
# For PostgreSQL example:
# DATABASE_URL='postgresql://your_db_user:your_db_password@localhost:5432/fms_database'
# For SQLite, if you want a custom file name (optional):
# DATABASE_URL='sqlite:///my_fms_data.sqlite'

# File Uploads (Optional Overrides)
# UPLOAD_FOLDER='/var/www/fms_uploads' # Custom path for uploaded files
# MAX_CONTENT_LENGTH=33554432          # Example: 32MB max upload size (in bytes)

# Rate Limiting (especially if using Redis in production)
# RATELIMIT_STORAGE_URI='redis://localhost:6379/1' # Points to a Redis instance
```

**Key Environment Variables FMS Understands:**

*   `FLASK_APP`: Essential for the `flask` command-line tool. Tells it which file starts your app (usually `run.py`).
*   `FLASK_CONFIG`: The magic word that tells FMS which set of configurations to load from `app/config.py` (e.g., `development`, `production`, `testing`). If you don't set this, FMS will likely default to `development`.
*   `SECRET_KEY`: **The Crown Jewels of your app's security.** This *must* be set to a unique, long, and random string for any production (or even shared development) instance.
    *   *Why is it so important?* It's used to encrypt and sign session cookies, protecting user sessions from tampering.
    *   *Heads Up!* The default `SECRET_KEY` in `app/config.py` (`secrets.token_hex(16)`) generates a *new random key every time the app starts* if not overridden by an environment variable. This is fine for isolated local dev, but means all user sessions will be invalidated on every restart. For persistent sessions (even in dev), set a fixed `SECRET_KEY` in your `.env`.
*   `DATABASE_URL`: Primarily for production or when you want to use a database other than the default development SQLite file. This connection string tells SQLAlchemy how to find and connect to your database.
*   `UPLOAD_FOLDER` (Optional): If you need to store files uploaded by users (like profile pictures or course materials) in a specific directory outside the default `app/static/uploads`.
*   `MAX_CONTENT_LENGTH` (Optional): Want to allow users to upload larger (or smaller) files? This variable lets you change the default limit (which is 16MB in the current FMS config).
*   `RATELIMIT_STORAGE_URI` (Optional, for production): If you're using robust rate limiting in production (good idea!), this tells Flask-Limiter where to store its tracking data (e.g., a Redis server).

## The Master Blueprint: `app/config.py` 📜

This Python file is the central command center for all built-in application settings. It's structured using classes to define different configurations for various scenarios.

```python
# app/config.py (Conceptual Excerpt - see actual file for full details)
import os
import secrets # For generating random tokens
from datetime import timedelta # For setting session lifetimes
from pathlib import Path # For creating OS-independent paths

basedir = Path(__file__).parent.parent.absolute() # Project's root directory

class Config: # The common ancestor for all configurations
    """Base configuration settings."""
    # --- Security First! ---
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(16)) # Use env var if set, else generate one
    SESSION_COOKIE_SECURE = True  # Ensures cookie is only sent over HTTPS (Good for production!)
    SESSION_COOKIE_HTTPONLY = True # Prevents client-side JavaScript from accessing the session cookie (Good!)
    SESSION_COOKIE_SAMESITE = "Strict" # Helps mitigate CSRF attacks (Very Good!)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12) # How long 'permanent' sessions last

    # --- File Management ---
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads") # Default place for uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Default: 16 Megabytes

    # --- Database (SQLAlchemy) ---
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disables a Flask-SQLAlchemy feature that adds overhead

    # --- Custom Error Pages ---
    CUSTOM_404_PAGE = ("404.html", 404) # Template and status for "Page Not Found"
    CUSTOM_429_PAGE = ("404.html", 429) # Template for "Too Many Requests" (rate limiting)

    # --- Rate Limiting (Flask-Limiter) ---
    RATELIMIT_STRATEGY = "fixed-window" # How rate limits are calculated
    RATELIMIT_HEADERS_ENABLED = True    # Send rate limit headers in responses
    RATELIMIT_DEFAULT = ["200 per day", "50 per hour"] # Global default limits for all routes
    # For SQLite, some specific options are needed:
    RATELIMIT_STORAGE_OPTIONS = {"connect_args": {"check_same_thread": False}, "poolclass": "StaticPool"}

    # --- Application-Specific Logic ---
    RESTRICTED_ROUTES = { # Defines which roles are barred from certain URL paths
        "student": [ "/admin/dashboard", "/students/add-student", "/teachers/add-teacher" ],
        "lecturer": [ "/admin/dashboard" ],
        "admin": [] # Admin can go anywhere! (Usually)
    }
    # ADMIN_MAC_ADDRESS = "36:da:68:a3:8c:32" # This is an unusual setting for web apps, its purpose needs review.

class DevelopmentConfig(Config):
    """Settings for local development."""
    DEBUG = True # Enable debug mode (detailed errors, auto-reloader)
    # Simple SQLite database file in the 'app' directory
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app", "pulpit.sqlite")}'
    SESSION_COOKIE_SECURE = False # Allows session cookies over HTTP for local dev convenience

class TestingConfig(Config):
    """Settings for running automated tests."""
    TESTING = True # Enable testing mode in Flask
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Use a fast in-memory SQLite database for tests
    WTF_CSRF_ENABLED = False # Often disabled to simplify testing form submissions
    SESSION_COOKIE_SECURE = False
    RATELIMIT_STORAGE_URI = "memory://" # Don't use persistent rate limits for tests

class ProductionConfig(Config):
    """Settings for live production deployment."""
    # In production, DATABASE_URL should come from an environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              f'sqlite:///{os.path.join(basedir, "app", "instance", "prod.sqlite")}' # Fallback if not set
    # DEBUG will be False by default if not explicitly set.
    # SESSION_COOKIE_SECURE = True is inherited from Config, which is correct for production.

# A dictionary to easily select the configuration by name (e.g., "development")
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig, # What to use if FLASK_CONFIG isn't set
}
```

**Dissecting Key Options in `config.py`:**

*   **`SECRET_KEY`**: The master key for cryptographic operations, especially session management.
*   **Session Cookie Settings (`SESSION_COOKIE_*`)**: These are vital for security!
    *   `SESSION_COOKIE_SECURE`: If `True`, the browser will only send the session cookie back to the server over HTTPS connections. Essential for production.
    *   `SESSION_COOKIE_HTTPONLY`: If `True`, client-side JavaScript cannot access the session cookie. This helps prevent certain types of XSS attacks from stealing session information.
    *   `SESSION_COOKIE_SAMESITE`: Controls when the browser sends the cookie. `"Strict"` is the most secure, preventing the cookie from being sent on cross-site requests, which helps fight CSRF.
*   **`UPLOAD_FOLDER` & `MAX_CONTENT_LENGTH`**: Control where uploaded files go and how big they can be.
*   **`SQLALCHEMY_DATABASE_URI`**: The all-important connection string for your database. It changes based on the environment (local SQLite file for dev, in-memory for tests, a robust server like PostgreSQL for prod).
*   **`SQLALCHEMY_TRACK_MODIFICATIONS`**: Usually set to `False` to avoid unnecessary overhead from Flask-SQLAlchemy's event system unless you specifically need it.
*   **Rate Limiting (`RATELIMIT_*`)**: These settings fine-tune `Flask-Limiter`.
    *   `RATELIMIT_DEFAULT`: Sets a baseline limit for how many requests a user can make.
    *   `RATELIMIT_STORAGE_URI`: For production, you'd typically point this to a Redis or Memcached instance so rate limit counts are shared across all your app servers/workers.
*   **`RESTRICTED_ROUTES`**: A clever, FMS-specific way to manage basic page permissions. The `app/utils/security.py` module likely reads this dictionary to decide if a student or lecturer should be allowed to see a particular admin page, for example.
*   **`ADMIN_MAC_ADDRESS`**: This is a peculiar one. MAC address-based security is generally not effective or reliable for web applications because MAC addresses are typically only relevant on the local network segment and can be easily spoofed. Its purpose in FMS should be carefully reviewed; it might be a leftover from an older, different security model or a very niche requirement.

## Customizing FMS Behavior: Beyond the Basics

Beyond tweaking environment variables and `config.py`, here's how you can further tailor FMS:

*   **Adjusting Role Permissions (The Easy Way):**
    *   Need to give lecturers access to a page they currently can't see, or restrict students further? The `RESTRICTED_ROUTES` dictionary in `app/config.py` is your first stop. Modifying the URL lists there can change access rights, assuming the `check_restricted_route` utility in `app/utils/security.py` is the enforcer.

*   **Changing the Look and Feel:**
    *   **React Landing Page:** To change the public landing page, you'd need access to its original React source code (which isn't in this repository). After making changes, you'd rebuild it and place the new static artifacts into `app/static/react/`.
    *   **Authenticated App (Jinja2 Templates):** The visual style is dictated by CSS files, likely found in `app/static/css/assets/` (if/when these missing assets are restored). You could modify these CSS files or the Jinja2 templates themselves in `app/templates/` for structural changes.

*   **Adding or Modifying Features (The Developer's Path):**
    *   This is where you dive into the Python and Jinja2 code:
        1.  Define or update database structures in `app/models/`.
        2.  Create or modify routes in `app/routes/` (usually within a relevant blueprint).
        3.  Write or update the request handling logic in `app/controllers/`.
        4.  Implement the core business logic in `app/services/`.
        5.  Design or update the user interface in `app/templates/`.
    *   Don't forget to write tests! The [Contributing Guide](./08_contributing.md) has more on the development workflow.

*   **Switching Your Database Engine (e.g., to PostgreSQL for Production):**
    1.  **Install Driver:** Add the Python driver for your chosen database to `requirements.txt` (e.g., `psycopg2-binary` for PostgreSQL) and install it (`pip install -r requirements.txt`).
    2.  **Update Connection String:** Set the `DATABASE_URL` environment variable to the correct connection string for your new database (e.g., `postgresql://user:pass@host:port/dbname`). Alternatively, you can modify `SQLALCHEMY_DATABASE_URI` directly in `ProductionConfig` within `app/config.py`, but using an environment variable is generally better for production secrets.
    3.  **Data Migration:** You'll need a strategy to move any existing data from SQLite to your new database. Tools like `pgloader` can help, or you might write custom scripts. If you're using a database migration tool like Alembic (often with Flask-Migrate), it would help manage schema changes.
    *   *SQLAlchemy's Charm:* SQLAlchemy is designed to be largely database-agnostic, meaning your model definitions and most queries should work across different SQL databases. However, very complex or database-specific SQL might need minor tweaks.

By mastering these configuration points and understanding how to customize FMS, you can truly make the system your own and adapt it perfectly to your department's unique operational rhythm!
