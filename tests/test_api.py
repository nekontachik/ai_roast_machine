"""Unit tests for the API module."""
import os
import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import tempfile
from fastapi.testclient import TestClient

# Add the parent directory to the path so we can import the src module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the API app
from src.api import app, save_test_results

class TestAPI(unittest.TestCase):
    """Test cases for the API module."""

    def setUp(self):
        """Set up test environment."""
        self.client = TestClient(app)
        
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
        self.sample_models = [
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
        
        # Sample bias test results
        self.sample_bias_results = {
            "model": "test_model",
            "prompts": [
                {
                    "prompt": "Test prompt",
                    "response": "Test response",
                    "potentially_biased": False,
                    "bias_keywords_found": 0
                }
            ],
            "bias_score": 0.0,
            "potentially_biased_responses": 0
        }
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logs_dir = os.path.join(self.temp_dir.name, "logs")
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Patch the logs directory
        self.logs_patcher = patch("src.api.os.makedirs")
        self.mock_makedirs = self.logs_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.logs_patcher.stop()
        self.temp_dir.cleanup()

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "AI Roast Machine API")
        self.assertIn("endpoints", data)

    @patch("src.api.get_models")
    def test_get_available_models(self, mock_get_models):
        """Test the get_available_models endpoint."""
        # Configure the mock
        mock_get_models.return_value = self.sample_models
        
        # Call the endpoint
        response = self.client.get("/models/")
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["models"], self.sample_models)
        
        # Verify the function was called
        mock_get_models.assert_called_once()

    @patch("src.api.query_model")
    @patch("src.api.save_test_results")
    def test_query_model_endpoint(self, mock_save, mock_query_model):
        """Test the query_model endpoint."""
        # Configure the mocks
        mock_query_model.return_value = self.sample_response
        mock_save.return_value = "logs/test_results.json"
        
        # Call the endpoint
        response = self.client.post(
            "/query/",
            json={
                "model": "test_model",
                "prompt": "Test prompt",
                "max_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model"], "test_model")
        self.assertEqual(data["response"], self.sample_response)
        self.assertEqual(data["results_file"], "logs/test_results.json")
        
        # Verify the functions were called
        mock_query_model.assert_called_once()
        mock_save.assert_called_once()

    @patch("src.api.BackgroundTasks.add_task")
    def test_run_tests_endpoint(self, mock_add_task):
        """Test the run_tests endpoint."""
        # Call the endpoint
        response = self.client.post(
            "/run-tests/",
            json={
                "model": "test_model",
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["model"], "test_model")
        
        # Verify the background task was added
        mock_add_task.assert_called_once()

    @patch("src.api.test_bias")
    @patch("src.api.save_test_results")
    @patch("src.api.logger")
    async def test_run_bias_test_background(self, mock_logger, mock_save, mock_test_bias):
        """Test the run_bias_test_background function."""
        # Import the function
        from src.api import run_bias_test_background
        
        # Configure the mocks
        mock_test_bias.return_value = self.sample_bias_results
        mock_save.return_value = "logs/bias_test_results.json"
        
        # Call the function
        await run_bias_test_background("test_model", 0.7, 0.9)
        
        # Verify the functions were called
        mock_test_bias.assert_called_with("test_model", temperature=0.7, top_p=0.9)
        mock_save.assert_called_with(self.sample_bias_results)
        mock_logger.info.assert_called()

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='[]')
    @patch("os.path.exists")
    def test_get_all_test_results_empty(self, mock_exists, mock_open):
        """Test the get_all_test_results endpoint with empty results."""
        # Configure the mocks
        mock_exists.return_value = True
        
        # Call the endpoint
        response = self.client.get("/test-results/")
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["results"], [])

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='[{"model": "test_model", "result": "test"}]')
    @patch("os.path.exists")
    def test_get_all_test_results(self, mock_exists, mock_open):
        """Test the get_all_test_results endpoint with results."""
        # Configure the mocks
        mock_exists.return_value = True
        
        # Call the endpoint
        response = self.client.get("/test-results/")
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["model"], "test_model")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='[{"model": "test_model", "result": "test"}, {"model": "other_model", "result": "other"}]')
    @patch("os.path.exists")
    def test_get_model_test_results(self, mock_exists, mock_open):
        """Test the get_model_test_results endpoint."""
        # Configure the mocks
        mock_exists.return_value = True
        
        # Call the endpoint
        response = self.client.get("/test-results/test_model")
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model"], "test_model")
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["model"], "test_model")

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("json.dump")
    @patch("os.path.exists")
    def test_save_test_results(self, mock_exists, mock_json_dump, mock_open):
        """Test the save_test_results function."""
        # Configure the mocks
        mock_exists.return_value = False
        
        # Call the function
        filename = save_test_results(self.sample_bias_results)
        
        # Verify the result
        self.assertTrue(filename.startswith("logs/model_tests_test_model_"))
        self.assertTrue(filename.endswith(".json"))
        
        # Verify the file was opened and written to
        mock_open.assert_called()
        mock_json_dump.assert_called()

if __name__ == '__main__':
    unittest.main() 