from flask import jsonify
from models.dest import destinations
from flasgger import swag_from


def destination_route(app):
    @app.route('/all-destination', methods=['GET'])
    @swag_from({
        'tags': ['Destination Service'],  # Categorize the endpoint
        'summary': 'Get All Destinations',
        'description': 'Retrieve a list of all available destinations.',
        'responses': {
            200: {
                'description': 'A list of destinations.',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'name': {
                                'type': 'string',
                                'example': 'Paris'
                            },
                            'description': {
                                'type': 'string',
                                'example': 'The City of Light'
                            },
                        },
                    },
                },
            },
            404: {
                'description': 'No destinations found.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'No destinations found.'
                        }
                    }
                }
            },
        }
    })
    def allDestination():
        if destinations:
            return jsonify(destinations), 200
        return jsonify({"msg": "No destinations found."}), 404
