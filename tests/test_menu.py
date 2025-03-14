"""Unit tests for the menu module."""
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import sys
import tempfile
import io

# Add the parent directory to the path so we can import the src module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.menu import (
    save_to_both_locations,
    generate_html_report,
    LoadingAnimation
)

class TestMenu(unittest.TestCase):
    """Test cases for the menu module."""

    def setUp(self):
        """Set up test environment."""
        # Sample data for testing
        self.sample_comparison_data = {
            "prompt": "Test prompt",
            "timestamp": "20250101_120000",
            "results": {
                "model1": "Response from model 1",
                "model2": "Response from model 2"
            }
        }
        
        self.sample_single_model_data = {
            "model": "test_model",
            "prompt": "Test prompt",
            "timestamp": "20250101_120000",
            "response": "Test response"
        }
        
        self.sample_bias_data = {
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
            "potentially_biased_responses": 0,
            "timestamp": "20250101_120000"
        }
        
        self.sample_meme_content = "Prompt: Test meme prompt\n\nTitle: Test Meme\nContent: This is a test meme"

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('json.dump')
    def test_save_to_both_locations_json(self, mock_json_dump, mock_exists, mock_file, mock_makedirs):
        """Test saving JSON data to both locations."""
        # Configure mocks
        mock_exists.return_value = False
        
        # Call the function
        result = save_to_both_locations(
            self.sample_comparison_data,
            "/app/test_results/test.json",
            "test_results/test.json",
            is_json=True
        )
        
        # Verify the result
        self.assertEqual(result, "test_results/test.json")
        
        # Verify directories were created
        mock_makedirs.assert_called_with("test_results", exist_ok=True)
        
        # Verify file was opened and written to
        mock_file.assert_called_with("test_results/test.json", "w")
        
        # Verify json.dump was called
        mock_json_dump.assert_called_once()

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_save_to_both_locations_text(self, mock_exists, mock_file, mock_makedirs):
        """Test saving text data to both locations."""
        # Configure mocks
        mock_exists.return_value = False
        
        # Call the function
        result = save_to_both_locations(
            self.sample_meme_content,
            "/app/memes/test.txt",
            "memes/test.txt",
            is_json=False
        )
        
        # Verify the result
        self.assertEqual(result, "memes/test.txt")
        
        # Verify directories were created
        mock_makedirs.assert_called_with("memes", exist_ok=True)
        
        # Verify file was opened and written to
        mock_file.assert_called_with("memes/test.txt", "w")
        handle = mock_file()
        handle.write.assert_called_with(self.sample_meme_content)

    def test_generate_html_report_comparison(self):
        """Test generating HTML report for model comparison."""
        # Call the function
        html = generate_html_report(self.sample_comparison_data, "comparison")
        
        # Verify the result contains expected elements
        self.assertIn("MODEL COMPARISON", html)
        self.assertIn("Test prompt", html)
        self.assertIn("model1", html)
        self.assertIn("model2", html)
        self.assertIn("Response from model 1", html)
        self.assertIn("Response from model 2", html)
        self.assertIn("20250101_120000", html)

    def test_generate_html_report_single_model(self):
        """Test generating HTML report for single model test."""
        # Call the function
        html = generate_html_report(self.sample_single_model_data, "single_model")
        
        # Verify the result contains expected elements
        self.assertIn("MODEL: test_model", html)
        self.assertIn("Test prompt", html)
        self.assertIn("Test response", html)
        self.assertIn("20250101_120000", html)

    def test_generate_html_report_bias(self):
        """Test generating HTML report for bias test."""
        # Call the function
        html = generate_html_report(self.sample_bias_data, "bias")
        
        # Verify the result contains expected elements
        self.assertIn("MODEL: test_model", html)
        self.assertIn("AI Roast Machine: Bias Test", html)
        self.assertIn("Test prompt", html)
        self.assertIn("Test response", html)
        self.assertIn("20250101_120000", html)
        self.assertIn("Bias Score", html)

    def test_generate_html_report_meme(self):
        """Test generating HTML report for meme."""
        # Call the function
        html = generate_html_report(self.sample_meme_content, "meme")
        
        # Verify the result contains expected elements
        self.assertIn("GENERATED MEME", html)
        self.assertIn("Test Meme", html)
        self.assertIn("Prompt: Test meme prompt", html)
        self.assertIn("This is a test meme", html)
        # Should not contain timestamp from data (it's a string)
        self.assertNotIn("20250101_120000", html)
        # But should contain a timestamp generated during the function call
        self.assertIn("Report generated on", html)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('threading.Thread')
    def test_loading_animation(self, mock_thread, mock_stdout):
        """Test the LoadingAnimation class."""
        # Create a loading animation
        animation = LoadingAnimation("test_model")
        
        # Start the animation
        animation.start()
        
        # Verify thread was started
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()
        
        # Verify animation is running
        self.assertTrue(animation.is_running)
        
        # Stop the animation
        animation.stop()
        
        # Verify animation is stopped
        self.assertFalse(animation.is_running)
        mock_thread.return_value.join.assert_called_once()

if __name__ == '__main__':
    unittest.main() 