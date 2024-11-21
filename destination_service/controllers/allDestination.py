from flask import Flask, request, jsonify
from models.dest import destinations
from flask_jwt_extended import jwt_required, get_jwt_identity

def destination_route(app):
    @app.route('/all-destination', methods=['GET'])
    def allDestination():
        if destinations:
            return jsonify(destinations), 200
        return jsonify({"msg": "No destinations found."}), 404