from flask import Flask, request, jsonify
from data.dest import destinations
from flask_jwt_extended import jwt_required, get_jwt_identity


def delete_route(app):
    @app.route('/destinations/<id>', methods=['DELETE'])
    def deleteDestination(id):
        # Check if the user is an Admin
        if request.headers.get('role') != 'Admin':
            return jsonify({"msg": "Unauthorized. Admins only."}), 403
        
        # Find the destination with the matching ID
        destination_to_delete = next((dest for dest in destinations if dest['id'] == id), None)
        
        if destination_to_delete:
            # If destination exists, remove it from the list
            destinations.remove(destination_to_delete)
            return jsonify({"msg": f"Destination {id} has been deleted."}), 200
        
        return jsonify({"msg": "Destination not found."}), 404
