from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from models.user import users


def register_route(app):
    @app.route('/register', methods=['POST'])
    def register():
        email = request.json.get('email')
        password = request.json.get('password')
        name = request.json.get('name')
        role = request.json.get('role', 'User')

        # Check if email is provided
        if not email or not password or not name:
            return jsonify({"msg": "Missing required fields."}), 400

        # Check if the user already exists
        for user in users:
            if email in user['email']:
                return jsonify({"msg": "User with this email already exists."}), 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user entry
        users.append({
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
        })

        return jsonify({"msg": "User registered successfully."}), 201