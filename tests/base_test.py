"""
Base test configuration and utilities
"""
import unittest
import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extention import db
from app.models import Customer, Mechanic, ServiceTicket, Inventory


class BaseTestCase(unittest.TestCase):
    """Base test case for all API tests"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create all database tables
        db.create_all()
        
        # Create test data
        self.create_test_data()
    
    def tearDown(self):
        """Tear down test fixtures after each test method"""
        # Close all database sessions properly
        db.session.close()
        db.session.remove()
        db.drop_all()
        
        # Close database connections
        db.engine.dispose()
        
        self.app_context.pop()
    
    def create_test_data(self):
        """Create common test data used across tests"""
        # Create test customer
        self.test_customer = Customer(
            name="Test Customer",
            email="test@customer.com",
            phone="555-123-4567",
            address="123 Test St"
        )
        self.test_customer.set_password("testpass123")
        
        # Create test mechanic
        self.test_mechanic = Mechanic(
            name="Test Mechanic",
            email="test@mechanic.com",
            phone="555-987-6543",
            specialty="Test Repair",
            hourly_rate=50.00
        )
        self.test_mechanic.set_password("mechpass123")
        
        # Add to database
        db.session.add(self.test_customer)
        db.session.add(self.test_mechanic)
        db.session.commit()
        
        # Store IDs for tests
        self.customer_id = self.test_customer.id
        self.mechanic_id = self.test_mechanic.id
    
    def get_customer_token(self, email="test@customer.com", password="testpass123"):
        """Helper method to get customer JWT token"""
        response = self.client.post('/customers/login', 
                                  json={'email': email, 'password': password})
        if response.status_code == 200:
            return response.get_json()['token']
        return None
    
    def get_mechanic_token(self, email="test@mechanic.com", password="mechpass123"):
        """Helper method to get mechanic JWT token"""
        response = self.client.post('/mechanics/login',
                                  json={'email': email, 'password': password})
        if response.status_code == 200:
            return response.get_json()['token']
        return None
    
    def get_auth_headers(self, token):
        """Helper method to get authorization headers"""
        return {'Authorization': f'Bearer {token}'}


if __name__ == '__main__':
    unittest.main()
