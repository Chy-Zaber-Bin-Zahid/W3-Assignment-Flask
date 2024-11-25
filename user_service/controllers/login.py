from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user import users
from flasgger import swag_from


def login_route(app):
    @app.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['User Service'],  # Categorize the endpoint
        'summary': 'User Login',
        'description': (
            'Allows a user to log in by providing valid email and password. '
            'Returns a JWT access token on successful authentication.'
        ),
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'description': 'Login credentials',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {
                            'type': 'string',
                            'example': 'user@example.com',
                            'description': 'The user\'s email address.'
                        },
                        'password': {
                            'type': 'string',
                            'example': 'SecureP@ssw0rd!',
                            'description': 'The user\'s password.'
                        }
                    },
                    'required': ['email', 'password']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Successful login with access token.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'access_token': {
                            'type': 'string',
                            'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV...'
                        }
                    }
                }
            },
            400: {
                'description': 'Bad Request: Missing or invalid fields.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Missing required field: email'
                        }
                    }
                }
            },
            401: {
                'description': 'Unauthorized: Invalid password.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Invalid password'
                        }
                    }
                }
            },
            404: {
                'description': 'User not found.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'User with this email does not exist'
                        }
                    }
                }
            }
        }
    })
    def login():
        data = request.json

        # Check if any extra fields are present
        allowed_fields = ['email', 'password']
        for field in data:
            if field not in allowed_fields:
                return jsonify({"msg": f"Invalid field: {field}"}), 400

        # Check if all required fields are provided
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "msg": f"Missing required field: {field}"
                    }), 400

        email = data['email']
        password = data['password']

        # Validate email type
        if not isinstance(email, str):
            return jsonify({"msg": "Email must be a string"}), 400

        # Simple email format validation
        if '@' not in email or '.' not in email:
            return jsonify({"msg": "Invalid email format"}), 400

        # Validate password length
        if len(password) < 8 or len(password) > 128:
            return jsonify({
                "msg": "Password must be between 8 and 128 characters long"
                }), 400

        # Find the user
        user = next((user for user in users if user['email'] == email), None)

        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(email))
            return jsonify(access_token=access_token), 200
        elif user:
            return jsonify({"msg": "Invalid password"}), 401
        else:
            return jsonify({"msg": "User with this email does not exist"}), 404
