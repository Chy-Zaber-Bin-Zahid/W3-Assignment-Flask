from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from data.user import users


def login_route(app):
    @app.route('/login', methods=['POST'])
    def login():
        email = request.json.get('email')
        password = request.json.get('password')
        user = next((user for user in users if user['email'] == email), None)
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity={'email': email, 'role': user['role']})
            return jsonify(access_token=access_token), 200
        return jsonify({"msg": "The user with the provided email does not exist."}), 404