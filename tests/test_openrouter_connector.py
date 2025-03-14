"""Unit tests for the OpenRouter connector module."""
import os
import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import tempfile

# Add the parent directory to the path so we can import the src module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.openrouter_connector import (
    query_model,
    get_available_models,
    extract_text_from_response,
    test_model_bias
)

class TestOpenRouterConnector(unittest.TestCase):
    """Test cases for the OpenRouter connector module."""

    def setUp(self):
        """Set up test environment."""
        # Create a mock environment variable for testing
        # Use patch.dict to properly mock the environment variable
        self.patcher = patch('src.openrouter_connector.OPENROUTER_API_KEY', 'test_api_key')
        self.patcher.start()
        
        # Sample API response
        self.sample_response = {
            "id": "response_id",
            "object": "chat.completion",
            "created": 1630000000,
            "model": "test_model",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "This is a test response."
                    },
                    "finish_reason": "stop"
                }
            ]
        }
        
        # Sample models response
        self.sample_models = {
            "data": [
                {
                    "id": "model1",
                    "name": "Model 1",
                    "description": "Test model 1",
                    "context_length": 4096
                },
                {
                    "id": "model2",
                    "name": "Model 2",
                    "description": "Test model 2",
                    "context_length": 8192
                }
            ]
        }

    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()

    @patch('requests.post')
    def test_query_model(self, mock_post):
        """Test the query_model function."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_response
        mock_post.return_value = mock_response
        
        # Call the function
        result = query_model(
            prompt="Test prompt",
            model="test_model",
            max_tokens=100,
            temperature=0.7,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        
        # Verify the result
        self.assertEqual(result, self.sample_response)
        
        # Verify the API was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test_api_key')
        
        # Verify request data
        request_data = kwargs['json']
        self.assertEqual(request_data['model'], 'test_model')
        self.assertEqual(request_data['messages'][0]['content'], 'Test prompt')
        self.assertEqual(request_data['max_tokens'], 100)
        self.assertEqual(request_data['temperature'], 0.7)
        self.assertEqual(request_data['top_p'], 0.9)
        self.assertEqual(request_data['frequency_penalty'], 0.1)
        self.assertEqual(request_data['presence_penalty'], 0.1)

    @patch('requests.get')
    def test_get_available_models(self, mock_get):
        """Test the get_available_models function."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_models
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_available_models()
        
        # Verify the result
        self.assertEqual(result, self.sample_models['data'])
        
        # Verify the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test_api_key')

    def test_extract_text_from_response(self):
        """Test the extract_text_from_response function."""
        # Test with valid response
        text = extract_text_from_response(self.sample_response)
        self.assertEqual(text, "This is a test response.")
        
        # Test with invalid response
        invalid_response = {"choices": []}
        text = extract_text_from_response(invalid_response)
        self.assertEqual(text, "")
        
        # Test with completely invalid response
        invalid_response = {"no_choices": True}
        text = extract_text_from_response(invalid_response)
        self.assertEqual(text, "")

    @patch('src.openrouter_connector.query_model')
    def test_model_bias(self, mock_query_model):
        """Test the test_model_bias function."""
        # Configure the mock
        mock_query_model.return_value = self.sample_response
        
        # Call the function with a custom prompt
        result = test_model_bias(
            model="test_model",
            prompts=["Test prompt"],
            max_tokens=100,
            temperature=0.7,
            top_p=0.9
        )
        
        # Verify the result structure
        self.assertEqual(result["model"], "test_model")
        self.assertEqual(len(result["prompts"]), 1)
        self.assertEqual(result["prompts"][0]["prompt"], "Test prompt")
        self.assertEqual(result["prompts"][0]["response"], "This is a test response.")
        self.assertFalse(result["prompts"][0]["potentially_biased"])
        self.assertEqual(result["bias_score"], 0.0)
        
        # Verify query_model was called correctly
        mock_query_model.assert_called_once()
        args, kwargs = mock_query_model.call_args
        self.assertEqual(kwargs['prompt'], 'Test prompt')
        self.assertEqual(kwargs['model'], 'test_model')
        self.assertEqual(kwargs['max_tokens'], 100)
        self.assertEqual(kwargs['temperature'], 0.7)
        self.assertEqual(kwargs['top_p'], 0.9)

if __name__ == '__main__':
    unittest.main() 