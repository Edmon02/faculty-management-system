import pytest


def test_homepage(client):
    """Test that the homepage loads."""
    response = client.get("/")
    assert response.status_code == 200


def test_login_page(client):
    """Test that the login page loads."""
    response = client.get("/login")
    assert response.status_code == 200


def test_invalid_login(client):
    """Test login with invalid credentials."""
    response = client.post("/login", data={"username": "invalid", "password": "invalid"})
    assert response.status_code == 500  # According to the original code, this returns 500


def test_restricted_routes_for_unauthenticated(client):
    """Test that unauthenticated users can't access restricted pages."""
    routes = ["/dashboard", "/students", "/teachers", "/subjects", "/exercises", "/waitingroom"]

    for route in routes:
        response = client.get(route)
        # Should redirect to login page
        assert response.status_code == 302


def test_logout(client, auth):
    """Test that logout works."""
    # First login
    auth.login()

    # Then logout
    response = auth.logout()

    # Should redirect to index page
    assert response.status_code == 302
