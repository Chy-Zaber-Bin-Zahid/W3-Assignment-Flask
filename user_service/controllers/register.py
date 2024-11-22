from flask import request, jsonify
from werkzeug.security import generate_password_hash
from models.user import users
from flasgger import swag_from


def register_route(app):
    @app.route('/register', methods=['POST'])
    @swag_from({
        'tags': ['User Service'],
        'summary': 'Register a New User',
        'description': (
            'Registers a new user in the system. '
            'The user must provide a unique email, name, and password. '
            'An optional "role" field can be included, defaulting to "User".'
        ),
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'email': {
                            'type': 'string', 'example': 'john.doe@example.com'
                            },
                        'password': {
                            'type': 'string', 'example': 'SecurePass123'
                            },
                        'name': {'type': 'string', 'example': 'John Doe'},
                        'role': {'type': 'string', 'example': 'Admin'}
                    },
                    'required': ['email', 'password', 'name']
                },
                'description': 'User registration data.'
            }
        ],
        'responses': {
            201: {
                'description': 'User registered successfully.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string', 'example': 'User '
                            'registered successfully.'
                            }
                    }
                }
            },
            400: {
                'description': 'Validation error.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string', 'example': 'Missing required '
                            'field: email'
                        }
                    }
                }
            },
            409: {
                'description': 'Conflict error when the user already exists.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string', 'example': 'User with this '
                            'email already exists.'
                        }
                    }
                }
            }
        }
    })
    def register():
        data = request.json
        # Check if all required fields are provided
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "msg": f"Missing required field: {field}"
                    }), 400

        email = data['email']
        password = data['password']
        name = data['name']
        role = data.get('role', 'User')

        # Validate types
        if not isinstance(email, str):
            return jsonify({"msg": "Email must be a string"}), 400
        if not isinstance(name, str):
            return jsonify({"msg": "Name must be a string"}), 400
        if not isinstance(role, str):
            return jsonify({"msg": "Role must be a string"}), 400

        # Simple email and password format validation
        if '@' not in email or '.' not in email:
            return jsonify({"msg": "Invalid email format"}), 400
        if len(password) < 8 or len(password) > 128:
            return jsonify({
                "msg": "Password must be between 8 and 128 characters long"
                }), 400

        # Check if the user already exists
        for user in users:
            if email == user['email']:
                return jsonify({
                    "msg": "User with this email already exists."
                    }), 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user entry
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
        }
        users.append(new_user)

        return jsonify({"msg": "User registered successfully."}), 201
