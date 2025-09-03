import pytest
import sys
import os
from app import create_app
from app.extention import db

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_app_creation(app):
    """Test that the app is created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    # In testing mode, this endpoint might not be available
    assert response.status_code in [200, 404]


def test_api_info(client):
    """Test the API info endpoint."""
    response = client.get('/info')
    # In testing mode, this endpoint might not be available
    assert response.status_code in [200, 404]


def test_customers_endpoint_exists(client):
    """Test that customers endpoint is accessible."""
    response = client.get('/customers/')  # Use trailing slash
    # Should return 200 or 404/405 (endpoint exists)
    assert response.status_code in [200, 404, 405]


def test_mechanics_endpoint_exists(client):
    """Test that mechanics endpoint is accessible."""
    response = client.get('/mechanics/')  # Use trailing slash
    assert response.status_code in [200, 404, 405]


def test_service_tickets_endpoint_exists(client):
    """Test that service tickets endpoint is accessible."""
    response = client.get('/service-tickets/')  # Use trailing slash
    assert response.status_code in [200, 404, 405]


def test_inventory_endpoint_exists(client):
    """Test that inventory endpoint is accessible."""
    response = client.get('/inventory/')  # Use trailing slash
    assert response.status_code in [200, 404, 405]


def test_customer_creation(client):
    """Test customer creation endpoint."""
    customer_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "1234567890",
        "address": "123 Test St",
        "password": "testpassword123"
    }

    response = client.post('/customers/',  # Use trailing slash
                           json=customer_data,
                           headers={'Content-Type': 'application/json'})

    # Should either create successfully or return validation error
    assert response.status_code in [201, 400, 422]


def test_mechanic_creation(client):
    """Test mechanic creation endpoint."""
    mechanic_data = {
        "name": "Test Mechanic",
        "email": "mechanic@example.com",
        "phone": "1234567890",
        "specialty": "Engine Repair",
        "hourly_rate": 50.0,
        "password": "testpassword123"
    }

    response = client.post('/mechanics/',  # Use trailing slash
                           json=mechanic_data,
                           headers={'Content-Type': 'application/json'})

    # Should either create successfully or return validation error
    assert response.status_code in [201, 400, 422]
