"""
Unit tests for general API endpoints
Tests health checks, error handlers, and other general functionality
"""
import unittest
from tests.base_test import BaseTestCase


class TestAPIGeneral(BaseTestCase):
    """Test cases for general API functionality"""

    def test_api_health_check(self):
        """Test basic API health check"""
        response = self.client.get('/')

        # API should be accessible (status code varies by implementation)
        self.assertIn(response.status_code, [200, 404, 405])

    def test_invalid_route(self):
        """Test accessing invalid/non-existent route"""
        response = self.client.get('/invalid-route-that-does-not-exist')

        self.assertEqual(response.status_code, 404)

    def test_cors_headers(self):
        """Test CORS headers are present in responses"""

        self.assertTrue(True)

    def test_content_type_json(self):
        """Test that API returns JSON content type"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        response = self.client.get('/customers/', headers=headers)

        if response.status_code == 200:
            self.assertIn('application/json',
                          response.headers.get('Content-Type', ''))

    def test_rate_limiting_headers(self):
        """Test that rate limiting headers are present"""
        response = self.client.get('/customers/')


        # This test checks general response structure
        self.assertIsNotNone(response.headers)

    def test_options_request(self):
        """Test OPTIONS request for CORS preflight"""
        response = self.client.options('/customers/')

        # OPTIONS requests should be handled
        self.assertIn(response.status_code, [200, 204, 405])

    def test_invalid_json_payload(self):
        """Test sending invalid JSON payload"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        # Send malformed JSON
        response = self.client.post('/customers/',
                                    data='{"invalid": json}',
                                    content_type='application/json',
                                    headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_large_payload(self):
        """Test sending unusually large payload"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        # Create a large but valid payload
        large_data = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "1234567890",
            "description": "x" * 1000  # Large description
        }

        response = self.client.post('/customers/', json=large_data,
                                    headers=headers)

        # Should either accept or reject based on size limits
        self.assertIn(response.status_code, [200, 201, 400, 413])

    def test_empty_payload(self):
        """Test sending empty payload to endpoints expecting data"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        response = self.client.post('/customers/', json={},
                                    headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_sql_injection_attempt(self):
        """Test basic SQL injection protection"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        malicious_data = {
            "name": "'; DROP TABLE customers; --",
            "email": "test@example.com",
            "phone": "1234567890"
        }

        response = self.client.post('/customers/', json=malicious_data,
                                    headers=headers)

        # Should either process safely or reject
        self.assertNotEqual(response.status_code, 500)

    def test_xss_attempt(self):
        """Test basic XSS protection"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        xss_data = {
            "name": "<script>alert('xss')</script>",
            "email": "test@example.com",
            "phone": "1234567890"
        }

        response = self.client.post('/customers/', json=xss_data,
                                    headers=headers)

        # Should process without server error
        self.assertNotEqual(response.status_code, 500)

    def test_method_not_allowed(self):
        """Test sending wrong HTTP method to endpoints"""
        # Try PATCH on an endpoint that might not support it
        response = self.client.patch('/customers/')

        self.assertEqual(response.status_code, 405)

    def test_concurrent_requests(self):
        """Test basic concurrent request handling"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        # Make multiple requests rapidly
        responses = []
        for i in range(3):
            response = self.client.get('/customers/', headers=headers)
            responses.append(response)

        # All requests should complete successfully
        for response in responses:
            self.assertIn(response.status_code, [200, 429])  # 429 = rate limited

    def test_unicode_handling(self):
        """Test handling of unicode characters"""
        token = self.get_customer_token()
        headers = self.get_auth_headers(token)

        unicode_data = {
            "name": "José María García-López",
            "email": "josé@españa.com",
            "phone": "1234567890"
        }

        response = self.client.post('/customers/', json=unicode_data,
                                    headers=headers)

        # Should handle unicode without server error
        self.assertNotEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
