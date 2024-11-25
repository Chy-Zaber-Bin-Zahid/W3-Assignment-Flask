import pytest
from main import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,  # Enables test mode
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()  # Provides a test client for making requests
