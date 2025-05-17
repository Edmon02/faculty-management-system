import os
import sqlite3
import tempfile

import pytest

from app import create_app
from app.models import get_db


@pytest.fixture
def app():
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
            "WTF_CSRF_ENABLED": False,
        }
    )

    # Create the database and load test data
    with app.app_context():
        # Initialize test database here
        conn = sqlite3.connect(db_path)
        with open(os.path.join(os.path.dirname(__file__), "test_data.sql"), "r") as f:
            conn.executescript(f.read())
        conn.close()

    yield app

    # Teardown - close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post("/login", data={"username": username, "password": password})

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
