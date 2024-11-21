from flask import Flask, request, jsonify
from data.dest import destinations


def destination_route(app):
    @app.route('/all-destination', methods=['GET'])
    def allDestination():
        if destinations:
            return jsonify(destinations), 200
        return jsonify({"msg": "No destinations found."}), 404