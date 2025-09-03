"""
Unit tests for Service Ticket endpoints
Tests all service ticket-related routes including positive and negative cases
"""
import unittest
from tests.base_test import BaseTestCase
from app.models import ServiceTicket, Inventory
from app.extention import db


class TestServiceTicketRoutes(BaseTestCase):
    """Test cases for service ticket management endpoints"""

    def setUp(self):
        """Set up additional test data for service tickets"""
        super().setUp()

        # Create test service ticket
        self.test_ticket = ServiceTicket(
            title="Test Service Ticket",
            description="Test description for service ticket",
            customer_id=self.customer_id,
            vehicle_info="2020 Test Car",
            estimated_cost=100.00,
            priority="Medium"
        )

        # Create test inventory item
        self.test_inventory = Inventory(
            name="Test Part",
            description="Test part description",
            price=25.99,
            quantity=10,
            category="Test Category"
        )

        db.session.add(self.test_ticket)
        db.session.add(self.test_inventory)
        db.session.commit()

        self.ticket_id = self.test_ticket.id
        self.inventory_id = self.test_inventory.id

    def test_create_service_ticket_success(self):
        """Test successful service ticket creation"""
        ticket_data = {
            "title": "Oil Change Service",
            "description": "Regular oil change and filter replacement",
            "customer_id": self.customer_id,
            "vehicle_info": "2019 Honda Civic",
            "estimated_cost": 75.00,
            "priority": "Medium"
        }

        response = self.client.post('/service-tickets/', json=ticket_data)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], ticket_data['title'])
        self.assertEqual(data['customer_id'], ticket_data['customer_id'])
        self.assertEqual(data['priority'], ticket_data['priority'])

    def test_create_service_ticket_missing_fields(self):
        """Test service ticket creation with missing required fields"""
        ticket_data = {
            "title": "Incomplete Ticket"
            # Missing description, customer_id
        }

        response = self.client.post('/service-tickets/', json=ticket_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_service_ticket_invalid_priority(self):
        """Test service ticket creation with invalid priority"""
        ticket_data = {
            "title": "Invalid Priority Ticket",
            "description": "Test description",
            "customer_id": self.customer_id,
            "priority": "InvalidPriority"
        }

        response = self.client.post('/service-tickets/', json=ticket_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_service_ticket_nonexistent_customer(self):
        """Test service ticket creation with non-existent customer"""
        ticket_data = {
            "title": "Orphan Ticket",
            "description": "Test description",
            "customer_id": 999,  # Non-existent customer ID
            "vehicle_info": "Test Vehicle"
        }

        response = self.client.post('/service-tickets/', json=ticket_data)

        # Service tickets can be created without valid customer (walk-ins)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['customer_id'], 999)
        self.assertIsNone(data['customer'])  # Customer relationship None

    def test_get_all_service_tickets(self):
        """Test retrieving all service tickets"""
        response = self.client.get('/service-tickets/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Check pagination structure
        self.assertIsInstance(data, dict)
        self.assertIn('service_tickets', data)
        self.assertIn('total', data)
        self.assertIn('pages', data)
        self.assertIn('current_page', data)

        # Check service tickets array
        self.assertIsInstance(data['service_tickets'], list)
        self.assertGreater(len(data['service_tickets']), 0)
        self.assertGreater(data['total'], 0)

    def test_assign_mechanic_to_ticket(self):
        """Test assigning a mechanic to a service ticket"""
        url = (f'/service-tickets/{self.ticket_id}/assign-mechanic/'
               f'{self.mechanic_id}')

        response = self.client.put(url)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_assign_nonexistent_mechanic(self):
        """Test assigning non-existent mechanic to ticket"""
        url = f'/service-tickets/{self.ticket_id}/assign-mechanic/999'

        response = self.client.put(url)

        self.assertEqual(response.status_code, 404)

    def test_assign_mechanic_to_nonexistent_ticket(self):
        """Test assigning mechanic to non-existent ticket"""
        url = f'/service-tickets/999/assign-mechanic/{self.mechanic_id}'

        response = self.client.put(url)

        self.assertEqual(response.status_code, 404)

    def test_remove_mechanic_from_ticket(self):
        """Test removing a mechanic from a service ticket"""
        # First assign mechanic
        assign_url = (f'/service-tickets/{self.ticket_id}/assign-mechanic/'
                      f'{self.mechanic_id}')
        self.client.put(assign_url)

        # Then remove mechanic
        remove_url = (f'/service-tickets/{self.ticket_id}/remove-mechanic/'
                      f'{self.mechanic_id}')
        response = self.client.put(remove_url)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_remove_unassigned_mechanic(self):
        """Test removing mechanic that wasn't assigned to ticket"""
        url = (f'/service-tickets/{self.ticket_id}/remove-mechanic/'
               f'{self.mechanic_id}')

        response = self.client.put(url)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_bulk_edit_ticket_mechanics(self):
        """Test bulk editing mechanics on a ticket (add/remove)"""
        edit_data = {
            "add_ids": [self.mechanic_id],
            "remove_ids": []
        }

        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit',
                                   json=edit_data)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['id'], self.ticket_id)

    def test_bulk_edit_with_invalid_mechanic_ids(self):
        """Test bulk edit with non-existent mechanic IDs"""
        edit_data = {
            "add_ids": [999, 998],  # Non-existent mechanic IDs
            "remove_ids": []
        }

        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit',
                                   json=edit_data)

        # Should still succeed but ignore non-existent IDs
        self.assertEqual(response.status_code, 200)

    def test_add_part_to_ticket(self):
        """Test adding an inventory part to a service ticket"""
        url = f'/service-tickets/{self.ticket_id}/add-part/{self.inventory_id}'

        response = self.client.put(url)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_add_nonexistent_part_to_ticket(self):
        """Test adding non-existent part to ticket"""
        url = f'/service-tickets/{self.ticket_id}/add-part/999'

        response = self.client.put(url)

        self.assertEqual(response.status_code, 404)

    def test_add_part_to_nonexistent_ticket(self):
        """Test adding part to non-existent ticket"""
        url = f'/service-tickets/999/add-part/{self.inventory_id}'

        response = self.client.put(url)

        self.assertEqual(response.status_code, 404)

    def test_add_duplicate_part_to_ticket(self):
        """Test adding the same part twice to a ticket"""
        url = f'/service-tickets/{self.ticket_id}/add-part/{self.inventory_id}'

        # Add part first time
        response1 = self.client.put(url)
        self.assertEqual(response1.status_code, 200)

        # Add same part second time
        response2 = self.client.put(url)
        self.assertEqual(response2.status_code, 400)
        data = response2.get_json()
        self.assertIn('message', data)


if __name__ == '__main__':
    unittest.main()
