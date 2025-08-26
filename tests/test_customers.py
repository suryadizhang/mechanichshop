"""
Unit tests for Customer endpoints
Tests all customer-related routes including positive and negative test cases
"""
import unittest
import json
from tests.base_test import BaseTestCase


class TestCustomerRoutes(BaseTestCase):
    """Test cases for customer management endpoints"""
    
    def test_create_customer_success(self):
        """Test successful customer creation"""
        customer_data = {
            "name": "New Customer",
            "email": "new@customer.com",
            "phone": "555-111-2222",
            "address": "456 New St",
            "password": "newpass123"
        }
        
        response = self.client.post('/customers/', json=customer_data)
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], customer_data['name'])
        self.assertEqual(data['email'], customer_data['email'])
        self.assertNotIn('password', data)  # Password should not be returned
    
    def test_create_customer_missing_required_fields(self):
        """Test customer creation with missing required fields"""
        customer_data = {
            "name": "Incomplete Customer"
            # Missing email, phone, password
        }
        
        response = self.client.post('/customers/', json=customer_data)
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_create_customer_invalid_email(self):
        """Test customer creation with invalid email format"""
        customer_data = {
            "name": "Bad Email Customer",
            "email": "invalid-email",
            "phone": "555-111-2222",
            "password": "testpass123"
        }
        
        response = self.client.post('/customers/', json=customer_data)
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_create_customer_duplicate_email(self):
        """Test customer creation with duplicate email"""
        customer_data = {
            "name": "Duplicate Email",
            "email": "test@customer.com",  # Already exists from test data
            "phone": "555-111-2222",
            "password": "testpass123"
        }
        
        response = self.client.post('/customers/', json=customer_data)
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_customer_login_success(self):
        """Test successful customer login"""
        login_data = {
            "email": "test@customer.com",
            "password": "testpass123"
        }
        
        response = self.client.post('/customers/login', json=login_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')
    
    def test_customer_login_invalid_email(self):
        """Test customer login with invalid email"""
        login_data = {
            "email": "nonexistent@customer.com",
            "password": "testpass123"
        }
        
        response = self.client.post('/customers/login', json=login_data)
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_customer_login_invalid_password(self):
        """Test customer login with invalid password"""
        login_data = {
            "email": "test@customer.com",
            "password": "wrongpassword"
        }
        
        response = self.client.post('/customers/login', json=login_data)
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_get_customers_with_pagination(self):
        """Test retrieving customers with pagination"""
        response = self.client.get('/customers/?page=1&per_page=5')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('customers', data)
        self.assertIn('pagination', data)
        self.assertIn('page', data['pagination'])
        self.assertIn('total', data['pagination'])
    
    def test_get_customer_by_id(self):
        """Test retrieving a specific customer by ID"""
        response = self.client.get(f'/customers/{self.customer_id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.customer_id)
        self.assertEqual(data['email'], "test@customer.com")
    
    def test_get_customer_nonexistent_id(self):
        """Test retrieving customer with non-existent ID"""
        response = self.client.get('/customers/999')
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_my_tickets_with_token(self):
        """Test retrieving customer's tickets with valid token"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)
        
        response = self.client.get('/customers/my-tickets', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
    
    def test_get_my_tickets_without_token(self):
        """Test retrieving customer's tickets without token"""
        response = self.client.get('/customers/my-tickets')
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_get_my_tickets_invalid_token(self):
        """Test retrieving customer's tickets with invalid token"""
        headers = self.get_auth_headers('invalid.token.here')
        
        response = self.client.get('/customers/my-tickets', headers=headers)
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_update_customer_with_token(self):
        """Test updating customer information with valid token"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)
        
        update_data = {
            "name": "Updated Customer Name",
            "address": "789 Updated St"
        }
        
        response = self.client.put(f'/customers/{self.customer_id}',
                                 json=update_data, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], update_data['name'])
        self.assertEqual(data['address'], update_data['address'])
    
    def test_update_customer_without_token(self):
        """Test updating customer without authentication token"""
        update_data = {
            "name": "Updated Customer Name"
        }
        
        response = self.client.put(f'/customers/{self.customer_id}',
                                 json=update_data)
        
        self.assertEqual(response.status_code, 401)
    
    def test_delete_customer_with_token(self):
        """Test deleting customer with valid token"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)
        
        response = self.client.delete(f'/customers/{self.customer_id}',
                                    headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
    
    def test_delete_customer_without_token(self):
        """Test deleting customer without authentication token"""
        response = self.client.delete(f'/customers/{self.customer_id}')
        
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
