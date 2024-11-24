import pytest
from main import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "JWT_SECRET_KEY": "test-secret",  # Add JWT_SECRET_KEY for testing
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()  # Provides a test client for making requests
