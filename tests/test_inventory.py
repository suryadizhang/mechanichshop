"""
Unit tests for Inventory endpoints
Tests all inventory-related routes including positive and negative test cases
"""
import unittest
from tests.base_test import BaseTestCase


class TestInventoryRoutes(BaseTestCase):
    """Test cases for inventory management endpoints"""

    def test_create_inventory_with_mechanic_token(self):
        """Test successful inventory creation with mechanic token"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Oil Filter Premium",
            "description": "High-quality oil filter for most vehicles",
            "price": 15.99,
            "quantity": 50,
            "category": "Filters",
            "supplier": "AutoParts Plus"
        }

        response = self.client.post('/inventory/', json=inventory_data,
                                    headers=headers)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], inventory_data['name'])
        self.assertEqual(data['price'], inventory_data['price'])
        self.assertEqual(data['category'], inventory_data['category'])

    def test_create_inventory_without_token(self):
        """Test inventory creation without authentication token"""
        inventory_data = {
            "name": "Unauthorized Item",
            "price": 10.99
        }

        response = self.client.post('/inventory/', json=inventory_data)

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_inventory_with_customer_token(self):
        """Test inventory creation with customer token (should fail)"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Customer Restricted Item",
            "price": 10.99
        }

        response = self.client.post('/inventory/', json=inventory_data,
                                    headers=headers)

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_inventory_missing_required_fields(self):
        """Test inventory creation with missing required fields"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Incomplete Item"
            # Missing required price field
        }

        response = self.client.post('/inventory/', json=inventory_data,
                                    headers=headers)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_inventory_negative_price(self):
        """Test inventory creation with negative price"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Negative Price Item",
            "price": -5.99
        }

        response = self.client.post('/inventory/', json=inventory_data,
                                    headers=headers)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_all_inventory(self):
        """Test retrieving all inventory items (no auth required)"""
        response = self.client.get('/inventory/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_inventory_by_id(self):
        """Test retrieving specific inventory item by ID"""
        # First create an inventory item
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Test Item for Retrieval",
            "price": 29.99
        }

        create_response = self.client.post('/inventory/', json=inventory_data,
                                           headers=headers)
        created_item = create_response.get_json()
        item_id = created_item['id']

        # Then retrieve it
        response = self.client.get(f'/inventory/{item_id}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], item_id)
        self.assertEqual(data['name'], inventory_data['name'])

    def test_get_nonexistent_inventory_item(self):
        """Test retrieving non-existent inventory item"""
        response = self.client.get('/inventory/999')

        self.assertEqual(response.status_code, 404)

    def test_update_inventory_with_mechanic_token(self):
        """Test updating inventory with mechanic token"""
        # First create an inventory item
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Item to Update",
            "price": 19.99,
            "quantity": 10
        }

        create_response = self.client.post('/inventory/', json=inventory_data,
                                           headers=headers)
        created_item = create_response.get_json()
        item_id = created_item['id']

        # Then update it
        update_data = {
            "name": "Updated Item Name",
            "price": 24.99,
            "quantity": 15
        }

        response = self.client.put(f'/inventory/{item_id}',
                                   json=update_data, headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], update_data['name'])
        self.assertEqual(data['price'], update_data['price'])
        self.assertEqual(data['quantity'], update_data['quantity'])

    def test_update_inventory_without_token(self):
        """Test updating inventory without authentication token"""
        update_data = {
            "name": "Unauthorized Update",
            "price": 99.99
        }

        response = self.client.put('/inventory/1', json=update_data)

        self.assertEqual(response.status_code, 401)

    def test_update_nonexistent_inventory_item(self):
        """Test updating non-existent inventory item"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        update_data = {
            "name": "Non-existent Item",
            "price": 50.00
        }

        response = self.client.put('/inventory/999', json=update_data,
                                   headers=headers)

        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_with_mechanic_token(self):
        """Test deleting inventory with mechanic token"""
        # First create an inventory item
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        inventory_data = {
            "name": "Item to Delete",
            "price": 5.99
        }

        create_response = self.client.post('/inventory/', json=inventory_data,
                                           headers=headers)
        created_item = create_response.get_json()
        item_id = created_item['id']

        # Then delete it
        response = self.client.delete(f'/inventory/{item_id}',
                                      headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_delete_inventory_without_token(self):
        """Test deleting inventory without authentication token"""
        response = self.client.delete('/inventory/1')

        self.assertEqual(response.status_code, 401)

    def test_delete_nonexistent_inventory_item(self):
        """Test deleting non-existent inventory item"""
        token = self.get_mechanic_token()
        headers = self.get_auth_headers(token)

        response = self.client.delete('/inventory/999', headers=headers)

        self.assertEqual(response.status_code, 404)

    def test_inventory_caching(self):
        """Test that inventory endpoints are cached"""
        # Make first request
        response1 = self.client.get('/inventory/')
        self.assertEqual(response1.status_code, 200)

        # Make second request (should be cached)
        response2 = self.client.get('/inventory/')
        self.assertEqual(response2.status_code, 200)

        # Responses should be identical due to caching
        self.assertEqual(response1.get_json(), response2.get_json())


if __name__ == '__main__':
    unittest.main()
