from unittest.mock import patch


def test_delete_destination_success(client):
    # Mock destinations data
    mock_destinations = [
        {"id": 1, "name": "Paris", "description": "The City of Light",
            "location": "Swiss Alps"},
        {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun",
            "location": "London"}
    ]

    # Patch the destinations data
    with patch('controllers.deleteDestination.destinations',
         mock_destinations):
        # Make a DELETE request as an Admin to delete destination with ID 1
        response = client.delete('/destinations/1', headers={'role': 'Admin'})
        # Assert the response status and the message
        assert response.status_code == 200
        assert response.json == {"msg": "Destination 1 has been deleted."}
        assert len(mock_destinations) == 1


def test_delete_destination_unauthorized_non_admin(client):
    # Mock destinations data
    mock_destinations = [
        {"id": 1, "name": "Paris", "description": "The City of Light",
            "location": "Swiss Alps"},
        {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun",
            "location": "London"}
    ]

    # Patch the destinations data
    with patch('controllers.deleteDestination.destinations',
         mock_destinations):
        # Make a DELETE request with a non-admin role
        response = client.delete('/destinations/1', headers={'role': 'User'})
        # Assert the response status and the message
        assert response.status_code == 403
        assert response.json == {"msg": "Unauthorized. Admins only."}
        assert len(mock_destinations) == 2


def test_delete_destination_not_found(client):
    # Mock destinations data
    mock_destinations = [
        {"id": 1, "name": "Paris", "description": "The City of Light",
         "location": "Swiss Alps"},
        {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun",
         "location": "London"}
    ]

    # Patch the destinations data
    with patch('controllers.deleteDestination.destinations',
         mock_destinations):
        # Make a DELETE request to a non-existing destination (ID 3)
        response = client.delete('/destinations/3', headers={'role': 'Admin'})
        # Assert the response status and the message
        assert response.status_code == 404
        assert response.json == {"msg": "Destination not found."}
        assert len(mock_destinations) == 2  # Ensure no destination was removed


def test_delete_destination_unauthorized_no_role(client):
    # Mock destinations data
    mock_destinations = [
        {"id": 1, "name": "Paris", "description": "The City of Light",
            "location": "Swiss Alps"},
        {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun",
            "location": "London"}
    ]

    # Patch the destinations data
    with patch('controllers.deleteDestination.destinations',
         mock_destinations):
        # Make a DELETE request without providing the 'role' header
        response = client.delete('/destinations/1')
        # Assert the response status and the message
        assert response.status_code == 403
        assert response.json == {"msg": "Unauthorized. Admins only."}
        assert len(mock_destinations) == 2
