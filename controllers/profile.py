from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from data.user import users

def profile_route(app):
    @app.route('/profile', methods=['GET'])
    @jwt_required()
    def profile():
        # Get the identity of the current user
        current_user = get_jwt_identity()
        
        # If we're using a dictionary in the identity like {'email': email, 'role': role}
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
                'role': user['role']
            }), 200
        else:
            # If no user is found, return an error
            return jsonify({'message': 'User not found'}), 404

