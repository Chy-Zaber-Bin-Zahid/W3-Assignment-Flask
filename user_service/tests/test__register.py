from werkzeug.security import check_password_hash
from unittest.mock import patch


# Mock users list for testing
mock_users = [
    {"email": "existing_user@example.com", "password": "hashed_password",
     "name": "Existing User", "role": "User"}
]


# Test case: Successful registration
def test_register_success(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "new_user@example.com",
            "password": "SecurePass123!",
            "name": "New User",
            "role": "Admin"
        })
        assert response.status_code == 201
        assert response.json == {"msg": "User registered successfully."}
        new_user = next(user for user in mock_users
                        if user["email"] == "new_user@example.com")
        assert new_user["name"] == "New User"
        assert new_user["role"] == "Admin"
        assert check_password_hash(new_user["password"], "SecurePass123!")


# Test case: Missing required field
def test_register_missing_field(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "new_user@example.com",
            # Missing 'password' field
            "name": "New User"
        })
        assert response.status_code == 400
        assert response.json == {"msg": "Missing required field: password"}


# Test case: Invalid email format
def test_register_invalid_email_format(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "invalid-email-format",
            "password": "SecurePass123!",
            "name": "New User"
        })
        assert response.status_code == 400
        assert response.json == {"msg": "Invalid email format"}


# Test case: Password too short
def test_register_short_password(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "new_user@example.com",
            "password": "short",
            "name": "New User"
        })
        assert response.status_code == 400
        assert response.json == {
            "msg": "Password must be between 8 and 128 characters long"
            }


# Test case: Password too long
def test_register_long_password(client):
    with patch('controllers.register.users', mock_users):
        long_password = "a" * 129
        response = client.post('/register', json={
            "email": "new_user@example.com",
            "password": long_password,
            "name": "New User"
        })
        assert response.status_code == 400
        assert response.json == {
            "msg": "Password must be between 8 and 128 characters long"
            }


# Test case: Duplicate email
def test_register_duplicate_email(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "existing_user@example.com",
            "password": "SecurePass123!",
            "name": "New User"
        })
        assert response.status_code == 409
        assert response.json == {"msg": "User with this email already exists."}


# Test case: Role field is optional and defaults to "User"
def test_register_role_optional(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "newUser@example.com",
            "password": "SecurePass123!",
            "name": "New User"
        })
        assert response.status_code == 201
        assert response.json == {"msg": "User registered successfully."}
        new_user = next(user for user in mock_users
                        if user["email"] == "newUser@example.com")
        assert new_user["role"] == "User"  # Default value


# Test case: Invalid role type
def test_register_invalid_role_type(client):
    with patch('controllers.register.users', mock_users):
        response = client.post('/register', json={
            "email": "new_user@example.com",
            "password": "SecurePass123!",
            "name": "New User",
            "role": 123  # Invalid type for role
        })
        assert response.status_code == 400
        assert response.json == {"msg": "Role must be a string"}
