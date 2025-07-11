"""
Unit tests for URL Shortener Lambda functions
"""

import unittest
import json
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add lambda directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))

# Import Lambda functions
import shortenr
import redirector

class TestShortenrFunction(unittest.TestCase):
    """Test cases for the URL shortening function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.valid_event = {
            'httpMethod': 'POST',
            'body': json.dumps({'long_url': 'https://example.com/test'})
        }
        self.context = Mock()
    
    @patch('shortenr.table')
    def test_valid_url_shortening(self, mock_table):
        """Test successful URL shortening"""
        # Mock DynamoDB response
        mock_table.get_item.return_value = {}  # No existing item
        mock_table.put_item.return_value = {}
        
        # Mock generate_unique_short_code
        with patch('shortenr.generate_unique_short_code', return_value='abc123'):
            response = shortenr.lambda_handler(self.valid_event, self.context)
        
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('short_url', body)
        self.assertIn('short_code', body)
    
    def test_invalid_json(self):
        """Test handling of invalid JSON"""
        invalid_event = {
            'httpMethod': 'POST',
            'body': 'invalid json'
        }
        
        response = shortenr.lambda_handler(invalid_event, self.context)
        self.assertEqual(response['statusCode'], 400)
    
    def test_missing_url(self):
        """Test handling of missing URL"""
        missing_url_event = {
            'httpMethod': 'POST',
            'body': json.dumps({})
        }
        
        response = shortenr.lambda_handler(missing_url_event, self.context)
        self.assertEqual(response['statusCode'], 400)
    
    def test_invalid_url_format(self):
        """Test handling of invalid URL format"""
        invalid_url_event = {
            'httpMethod': 'POST',
            'body': json.dumps({'long_url': 'not-a-valid-url'})
        }
        
        response = shortenr.lambda_handler(invalid_url_event, self.context)
        self.assertEqual(response['statusCode'], 400)
    
    def test_options_request(self):
        """Test CORS preflight request"""
        options_event = {
            'httpMethod': 'OPTIONS'
        }
        
        response = shortenr.lambda_handler(options_event, self.context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
    
    def test_url_validation(self):
        """Test URL validation function"""
        # Valid URLs
        self.assertTrue(shortenr.is_valid_url('https://example.com'))
        self.assertTrue(shortenr.is_valid_url('http://test.org/path'))
        self.assertTrue(shortenr.is_valid_url('https://sub.domain.com:8080/path?query=1'))
        
        # Invalid URLs
        self.assertFalse(shortenr.is_valid_url('not-a-url'))
        self.assertFalse(shortenr.is_valid_url('ftp://example.com'))
        self.assertFalse(shortenr.is_valid_url(''))
    
    def test_short_code_generation(self):
        """Test short code generation"""
        # Test default length
        code = shortenr.generate_short_code()
        self.assertTrue(3 <= len(code) <= 8)
        self.assertTrue(code.isalnum())
        
        # Test specific length
        code = shortenr.generate_short_code(5)
        self.assertEqual(len(code), 5)
        self.assertTrue(code.isalnum())

class TestRedirectorFunction(unittest.TestCase):
    """Test cases for the URL redirection function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.valid_event = {
            'pathParameters': {'short_code': 'abc123'}
        }
        self.context = Mock()
    
    @patch('redirector.table')
    def test_successful_redirect(self, mock_table):
        """Test successful URL redirection"""
        # Mock DynamoDB response
        mock_table.get_item.return_value = {
            'Item': {
                'short_code': 'abc123',
                'long_url': 'https://example.com/test'
            }
        }
        mock_table.update_item.return_value = {}
        
        response = redirector.lambda_handler(self.valid_event, self.context)
        
        self.assertEqual(response['statusCode'], 301)
        self.assertEqual(response['headers']['Location'], 'https://example.com/test')
    
    @patch('redirector.table')
    def test_short_code_not_found(self, mock_table):
        """Test handling of non-existent short code"""
        # Mock DynamoDB response - no item found
        mock_table.get_item.return_value = {}
        
        response = redirector.lambda_handler(self.valid_event, self.context)
        
        self.assertEqual(response['statusCode'], 404)
        body = json.loads(response['body'])
        self.assertIn('error', body)
    
    def test_missing_path_parameters(self):
        """Test handling of missing path parameters"""
        invalid_event = {}
        
        response = redirector.lambda_handler(invalid_event, self.context)
        self.assertEqual(response['statusCode'], 400)
    
    def test_invalid_short_code_format(self):
        """Test handling of invalid short code format"""
        invalid_event = {
            'pathParameters': {'short_code': 'invalid@code!'}
        }
        
        response = redirector.lambda_handler(invalid_event, self.context)
        self.assertEqual(response['statusCode'], 400)
    
    def test_short_code_validation(self):
        """Test short code validation function"""
        # Valid short codes
        self.assertTrue(redirector.is_valid_short_code('abc123'))
        self.assertTrue(redirector.is_valid_short_code('XYZ'))
        self.assertTrue(redirector.is_valid_short_code('12345678'))
        
        # Invalid short codes
        self.assertFalse(redirector.is_valid_short_code('ab'))  # Too short
        self.assertFalse(redirector.is_valid_short_code('123456789'))  # Too long
        self.assertFalse(redirector.is_valid_short_code('abc@123'))  # Invalid characters
        self.assertFalse(redirector.is_valid_short_code(''))  # Empty

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    @patch('shortenr.table')
    @patch('redirector.table')
    def test_end_to_end_flow(self, mock_redirector_table, mock_shortenr_table):
        """Test complete flow: create short URL then redirect"""
        # Mock shortenr
        mock_shortenr_table.get_item.return_value = {}
        mock_shortenr_table.put_item.return_value = {}
        
        # Create short URL
        create_event = {
            'httpMethod': 'POST',
            'body': json.dumps({'long_url': 'https://example.com/test'})
        }
        
        with patch('shortenr.generate_unique_short_code', return_value='test123'):
            create_response = shortenr.lambda_handler(create_event, Mock())
        
        self.assertEqual(create_response['statusCode'], 200)
        create_body = json.loads(create_response['body'])
        short_code = create_body['short_code']
        
        # Mock redirector
        mock_redirector_table.get_item.return_value = {
            'Item': {
                'short_code': short_code,
                'long_url': 'https://example.com/test'
            }
        }
        mock_redirector_table.update_item.return_value = {}
        
        # Test redirect
        redirect_event = {
            'pathParameters': {'short_code': short_code}
        }
        
        redirect_response = redirector.lambda_handler(redirect_event, Mock())
        
        self.assertEqual(redirect_response['statusCode'], 301)
        self.assertEqual(redirect_response['headers']['Location'], 'https://example.com/test')

if __name__ == '__main__':
    unittest.main()
