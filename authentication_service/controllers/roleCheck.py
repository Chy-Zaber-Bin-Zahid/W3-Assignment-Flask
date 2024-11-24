from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from models.user import users


def role_route(app):
    @app.route('/role-check', methods=['GET'])
    @jwt_required()
    @swag_from({
        'tags': ['Authentication Service'],
        'description': 'Check if the current user has an '
        'Admin role based on the JWT token.',
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
            '200': {
                'description': 'Access granted to Admin user.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Access granted. You are an Admin.'
                        }
                    }
                }
            },
            '403': {
                'description': 'Access denied, user is not an Admin.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Access denied. Admins only.'
                        }
                    }
                }
            },
            '404': {
                'description': 'User not found.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'User not found.'
                        }
                    }
                }
            }
        }
    })
    def checkRole():
        # Get the identity (email) from the JWT token
        current_email = get_jwt_identity()

        # Find the user in the users list
        user = next(
            (user for user in users if user['email'] == current_email),
            None)

        if user:
            if user.get('role') == 'Admin':
                return jsonify(
                    {"msg": "Access granted. You are an Admin."}
                    ), 200
            else:
                return jsonify({"msg": "Access denied. Admins only."}), 403
        return jsonify({"msg": "User not found."}), 404
