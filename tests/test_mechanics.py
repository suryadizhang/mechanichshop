"""
Unit tests for Mechanic endpoints
Tests all mechanic-related routes including positive and negative test cases
"""
import unittest
from tests.base_test import BaseTestCase


class TestMechanicRoutes(BaseTestCase):
    """Test cases for mechanic management endpoints"""

    def test_create_mechanic_success(self):
        """Test successful mechanic creation"""
        mechanic_data = {
            "name": "New Mechanic",
            "email": "new@mechanic.com",
            "phone": "555-333-4444",
            "specialty": "Brake Repair",
            "hourly_rate": 65.00,
            "password": "mechanicpass123"
        }

        response = self.client.post('/mechanics/', json=mechanic_data)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], mechanic_data['name'])
        self.assertEqual(data['email'], mechanic_data['email'])
        self.assertEqual(data['specialty'], mechanic_data['specialty'])
        self.assertNotIn('password', data)

    def test_create_mechanic_missing_required_fields(self):
        """Test mechanic creation with missing required fields"""
        mechanic_data = {
            "name": "Incomplete Mechanic"
            # Missing email, phone, specialty, hourly_rate, password
        }

        response = self.client.post('/mechanics/', json=mechanic_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_mechanic_invalid_email(self):
        """Test mechanic creation with invalid email format"""
        mechanic_data = {
            "name": "Bad Email Mechanic",
            "email": "invalid-email",
            "phone": "555-333-4444",
            "specialty": "Test Repair",
            "hourly_rate": 50.00,
            "password": "mechanicpass123"
        }

        response = self.client.post('/mechanics/', json=mechanic_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_mechanic_negative_hourly_rate(self):
        """Test mechanic creation with negative hourly rate"""
        mechanic_data = {
            "name": "Negative Rate Mechanic",
            "email": "negative@mechanic.com",
            "phone": "555-333-4444",
            "specialty": "Test Repair",
            "hourly_rate": -10.00,
            "password": "mechanicpass123"
        }

        response = self.client.post('/mechanics/', json=mechanic_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_mechanic_login_success(self):
        """Test successful mechanic login"""
        login_data = {
            "email": "test@mechanic.com",
            "password": "mechpass123"
        }

        response = self.client.post('/mechanics/login', json=login_data)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')

    def test_mechanic_login_invalid_credentials(self):
        """Test mechanic login with invalid credentials"""
        login_data = {
            "email": "test@mechanic.com",
            "password": "wrongpassword"
        }

        response = self.client.post('/mechanics/login', json=login_data)

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_all_mechanics(self):
        """Test retrieving all mechanics"""
        response = self.client.get('/mechanics/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Check pagination structure
        self.assertIsInstance(data, dict)
        self.assertIn('mechanics', data)
        self.assertIn('total', data)
        self.assertIn('pages', data)
        self.assertIn('current_page', data)

        # Check mechanics array
        self.assertIsInstance(data['mechanics'], list)
        self.assertGreater(len(data['mechanics']), 0)
        self.assertGreater(data['total'], 0)

    def test_get_mechanics_by_tickets(self):
        """Test advanced query - mechanics ordered by ticket count"""
        response = self.client.get('/mechanics/by-tickets')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

        # Check if ticket_count is included in response
        if len(data) > 0:
            self.assertIn('ticket_count', data[0])

    def test_update_mechanic_with_token(self):
        """Test updating mechanic with valid token"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        update_data = {
            "name": "Updated Mechanic Name",
            "specialty": "Updated Specialty",
            "hourly_rate": 75.00
        }

        response = self.client.put(f'/mechanics/{self.mechanic_id}',
                                 json=update_data, headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], update_data['name'])
        self.assertEqual(data['specialty'], update_data['specialty'])

    def test_update_mechanic_without_token(self):
        """Test updating mechanic without authentication token"""
        update_data = {
            "name": "Updated Mechanic Name"
        }

        response = self.client.put(f'/mechanics/{self.mechanic_id}',
                                 json=update_data)

        self.assertEqual(response.status_code, 401)

    def test_update_mechanic_invalid_token(self):
        """Test updating mechanic with invalid token"""
        headers = self.get_auth_headers('invalid.token.here')

        update_data = {
            "name": "Updated Mechanic Name"
        }

        response = self.client.put(f'/mechanics/{self.mechanic_id}',
                                 json=update_data, headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_delete_mechanic_with_token(self):
        """Test deleting mechanic with valid token"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        response = self.client.delete(f'/mechanics/{self.mechanic_id}',
                                    headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_delete_mechanic_without_token(self):
        """Test deleting mechanic without authentication token"""
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')

        self.assertEqual(response.status_code, 401)

    def test_delete_nonexistent_mechanic(self):
        """Test deleting non-existent mechanic"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        response = self.client.delete('/mechanics/999', headers=headers)

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
