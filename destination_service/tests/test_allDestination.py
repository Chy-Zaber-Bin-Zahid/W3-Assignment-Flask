from unittest.mock import patch


# Test the successful retrieval of destinations
def test_all_destinations_success(client):
    # Mock destinations data
    mock_destinations = [
        {"id": 1, "name": "Paris", "description": "The City of Light",
         "location": "Swiss Alps"},
        {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun",
         "location": "London"},
    ]

    # Mock the destinations import
    with patch('controllers.allDestination.destinations', mock_destinations):
        response = client.get('/all-destination')
        print(response)

        assert response.status_code == 200
        assert response.json == mock_destinations


# Test the case where no destinations are available
def test_all_destinations_empty(client):
    # Mock an empty destinations list
    with patch('controllers.allDestination.destinations', []):
        response = client.get('/all-destination')

        assert response.status_code == 404
        assert response.json == {"msg": "No destinations found."}
