from flask import Flask, request, jsonify
from data.dest import destinations
from flask_jwt_extended import jwt_required, get_jwt_identity

def destination_route(app):
    @app.route('/all-destination', methods=['GET'])
    def allDestination():
        if destinations:
            return jsonify(destinations), 200
        return jsonify({"msg": "No destinations found."}), 404

    
    @app.route('/destinations/<id>', methods=['DELETE'])
    @jwt_required()
    def deleteDestination(id):
        current_user = get_jwt_identity()
        
        # Check if the user is an Admin
        if current_user['role'] != 'Admin':
            return jsonify({"msg": "Unauthorized. Admins only."}), 403
        
        # Check if the destination exists
        if id in destinations:
            destinations.pop(id)
            return jsonify({"msg": f"Destination {id} has been deleted."}), 200
        
        return jsonify({"msg": "Destination not found."}), 404