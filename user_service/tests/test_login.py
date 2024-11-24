from unittest.mock import patch
from werkzeug.security import generate_password_hash


# Mock user data
mock_users = [
    {"email": "user@example.com",
     "password": generate_password_hash("SecureP@ssw0rd!")},
    {"email": "admin@example.com",
     "password": generate_password_hash("AdminP@ss123!")}
]


# Test case: Successful login
def test_login_success(client):
    with patch('controllers.login.users', mock_users):
        response = client.post('/login', json={
            "email": "user@example.com",
            "password": "SecureP@ssw0rd!"
        })
        assert response.status_code == 200
        assert "access_token" in response.json


# Test case: Missing required fields
def test_login_missing_field(client):
    with patch('controllers.login.users', mock_users):
        response = client.post('/login', json={
            "email": "user@example.com"
            # Missing 'password'
        })
        assert response.status_code == 400
        assert response.json == {"msg": "Missing required field: password"}


# Test case: Invalid email format
def test_login_invalid_email_format(client):
    with patch('controllers.login.users', mock_users):
        response = client.post('/login', json={
            "email": "userexample.com",  # Invalid email
            "password": "SecureP@ssw0rd!"
        })
        assert response.status_code == 400
        assert response.json == {"msg": "Invalid email format"}


# Test case: Password too short
def test_login_short_password(client):
    with patch('controllers.login.users', mock_users):
        response = client.post('/login', json={
            "email": "user@example.com",
            "password": "short"  # Password too short
        })
        assert response.status_code == 400
        assert response.json == {
            "msg": "Password must be between 8 and 128 characters long"
        }


# Test case: Non-existent user
def test_login_user_not_found(client):
    with patch('controllers.login.users', mock_users):
        response = client.post('/login', json={
            "email": "unknown@example.com",  # Non-existent user
            "password": "SecureP@ssw0rd!"
        })
        assert response.status_code == 404
        assert response.json == {"msg": "User with this email does not exist"}


# Test case: Incorrect password
def test_login_invalid_password(client):
    with patch('controllers.login.users', mock_users):
        response = client.post('/login', json={
            "email": "user@example.com",
            "password": "WrongPassword123!"  # Incorrect password
        })
        assert response.status_code == 401
        assert response.json == {"msg": "Invalid password"}
