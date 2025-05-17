# from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

# Initialize extensions
# cors = CORS()
limiter = Limiter(
    get_remote_address,
    default_limits=["10000 per day", "1000 per hour"],
    storage_uri="memory://",
)
csrf = CSRFProtect()


def init_extensions(app):
    """Initialize Flask extensions"""
    # cors.init_app(app, origins=["http://localhost:3000/"])
    limiter.init_app(app)
    csrf.init_app(app)
