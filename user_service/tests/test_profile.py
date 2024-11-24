from unittest.mock import patch
from flask_jwt_extended import create_access_token


# Mock users list for testing
mock_users = [
    {"email": "existing_user@example.com", "password": "hashed_password",
     "name": "Existing User", "role": "Admin"}
]


# Test case: Successful profile retrieval
def test_profile_success(client, app):
    with patch('controllers.profile.users', mock_users):
        response = client.post('/register', json={
            "email": "new_user@example.com",
            "password": "SecurePass123!",
            "name": "New User",
            "role": "Admin"
        })
        assert response.status_code == 201
        # Ensure the app context is pushed before calling create_access_token
        with app.app_context():  # Ensures the app context is active
            # Create a valid JWT token for the mock user
            access_token = create_access_token(identity="new_user@example.com")

    # Use the generated token to make an authenticated request
    response = client.get('/profile', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200


# Test case: Missing or invalid JWT token
def test_profile_missing_token(client):
    response = client.get('/profile')

    assert response.status_code == 401
    assert response.json == {'msg': 'Missing Authorization Header'}
