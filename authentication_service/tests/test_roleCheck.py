from flask_jwt_extended import create_access_token
from unittest.mock import patch


# Mock user data
mock_users = [
    {"email": "admin@example.com", "role": "Admin"},
    {"email": "user@example.com", "role": "User"}
]


# Test case: Admin access granted
def test_role_check_admin(client, app):
    with app.app_context():  # Use app context for JWT token generation
        with patch('controllers.roleCheck.users', mock_users):
            # Generate a valid token for the admin
            access_token = create_access_token(identity="admin@example.com")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = client.get('/role-check', headers=headers)
            assert response.status_code == 200
            assert response.json == {
                "msg": "Access granted. You are an Admin."
                }


# Test case: User access denied
def test_role_check_non_admin(client, app):
    with app.app_context():  # Use app context for JWT token generation
        with patch('controllers.roleCheck.users', mock_users):
            # Generate a valid token for a regular user
            access_token = create_access_token(identity="user@example.com")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = client.get('/role-check', headers=headers)
            assert response.status_code == 403
            assert response.json == {"msg": "Access denied. Admins only."}


# Test case: User not found
def test_role_check_user_not_found(client, app):
    with app.app_context():  # Use app context for JWT token generation
        with patch('controllers.roleCheck.users', mock_users):
            # Generate a valid token for a non-existent user
            access_token = create_access_token(identity="unknown@example.com")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = client.get('/role-check', headers=headers)
            assert response.status_code == 404
            assert response.json == {"msg": "User not found."}


# Test case: Missing Authorization header
def test_role_check_missing_token(client):
    response = client.get('/role-check')  # No Authorization header
    assert response.status_code == 401
    assert "Missing Authorization Header" in response.json.get("msg", "")
