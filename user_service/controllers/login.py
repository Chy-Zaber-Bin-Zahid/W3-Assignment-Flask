from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import users

def login_route(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json

        # Check if all required fields are provided
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"msg": f"Missing required field: {field}"}), 400

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
            return jsonify({"msg": "Password must be between 8 and 128 characters long"}), 400

        # Find the user
        user = next((user for user in users if user['email'] == email), None)

        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(email))
            return jsonify(access_token=access_token), 200
        elif user:
            return jsonify({"msg": "Invalid password"}), 401
        else:
            return jsonify({"msg": "User with this email does not exist"}), 404