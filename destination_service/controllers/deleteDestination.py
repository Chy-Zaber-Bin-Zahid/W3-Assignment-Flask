from flask import request, jsonify
from models.dest import destinations
from flasgger import swag_from


def delete_route(app):
    @app.route('/destinations/<int:id>', methods=['DELETE'])
    @swag_from({
        'tags': ['Destination Service'],
        'summary': 'Delete a Destination',
        'description': (
            'Delete a destination by its ID. '
            'Only Admin users are allowed to perform this action.'
        ),
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'The ID of the destination to delete',
                'example': 1
            },
            {
                'name': 'role',
                'in': 'header',
                'type': 'string',
                'required': True,
                'description': 'The role of the user. Must be "Admin".',
                'example': 'Admin'
            }
        ],
        'responses': {
            200: {
                'description': 'Destination successfully deleted.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Destination 1 has been deleted.'
                        }
                    }
                }
            },
            403: {
                'description': 'Unauthorized. Only '
                'Admins can perform this action.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Unauthorized. Admins only.'
                        }
                    }
                }
            },
            404: {
                'description': 'Destination not found.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'msg': {
                            'type': 'string',
                            'example': 'Destination not found.'
                        }
                    }
                }
            }
        }
    })
    def deleteDestination(id):
        # Check if the user is an Admin
        if request.headers.get('role') != 'Admin':
            return jsonify({"msg": "Unauthorized. Admins only."}), 403
        # Find the destination with the matching ID
        destination_to_delete = next(
            (dest for dest in destinations if dest['id'] == id), None
            )
        if destination_to_delete:
            # If destination exists, remove it from the list
            destinations.remove(destination_to_delete)
            return jsonify({"msg": f"Destination {id} has been deleted."}), 200
        return jsonify({"msg": "Destination not found."}), 404
