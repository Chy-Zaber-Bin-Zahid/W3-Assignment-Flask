from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import users
from flasgger import swag_from


def profile_route(app):
    @app.route('/profile', methods=['GET'])
    @jwt_required()
    @swag_from({
        'tags': ['User Service'],  # Categorizing under "User Profile"
        'summary': 'Get User Profile',
        'description': (
            'Retrieves the profile information of the '
            'currently authenticated user. '
            'Requires a valid JWT token in the Authorization header.'
        ),
        'parameters': [
            {
                'name': 'Authorization',
                'in': 'header',
                'type': 'string',
                'required': True,
                'description': 'Bearer token for authentication. '
                'Example: "Bearer <JWT_TOKEN>"',
                'example': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
            }
        ],
        'responses': {
            200: {
                'description': 'Profile retrieved successfully.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'example': 'John Doe'},
                        'email': {
                            'type': 'string', 'example': 'john.doe@example.com'
                            },
                        'role': {'type': 'string', 'example': 'Admin'}
                    }
                }
            },
            404: {
                'description': 'User not found.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string', 'example': 'User not found'
                            }
                    }
                }
            },
            401: {
                'description': 'Unauthorized: Missing or invalid JWT token.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string', 'example': 'Missing '
                            'Authorization Header'
                            }
                    }
                }
            }
        }
    })
    def profile():
        # Get the identity of the current user
        current_user = get_jwt_identity()
        if isinstance(current_user, dict):
            email = current_user.get('email')
        else:
            # If we're just storing the email as a string in the identity
            email = current_user

        # Find the user in our database
        user = next((user for user in users if user['email'] == email), None)
        if user:
            # Return the user information
            return jsonify({
                'name': user['name'],
                'email': user['email'],
                'password': user['password'],
                'role': user['role']
            }), 200
        else:
            # If no user is found, return an error
            return jsonify({'message': 'User not found'}), 404
