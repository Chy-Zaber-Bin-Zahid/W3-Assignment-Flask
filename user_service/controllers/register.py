from flask import request, jsonify
from werkzeug.security import generate_password_hash
from models.user import users


def register_route(app):
    @app.route('/register', methods=['POST'])
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

        # Simple email format validation
        if '@' not in email or '.' not in email:
            return jsonify({"msg": "Invalid email format"}), 400

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
