#!/usr/bin/env python
"""Test script for AI Roast Machine."""
import os
import json
import logging
import sys

# Configure basic logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs("test_results", exist_ok=True)
os.makedirs("memes", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Import only what we need
try:
    from src.config import config
    from src.utils_helpers import save_json
    from src.roast_generator import generate_model_roast
    from src.meme_generator import generate_model_meme
except ImportError as e:
    logger.error(f"Error importing modules: {str(e)}")
    sys.exit(1)


def main():
    """Run a test of the AI Roast Machine."""
    logger.info(f"Starting AI Roast Machine test")
    print(f"✅ Testing AI Roast Machine...")

    # Test parameters
    model_name = "gpt2"
    model_type = "text-generation"
    test_output = "test_results/test_results.json"
    roast_output = "test_results/roast_results.json"
    meme_output = "memes/meme.png"

    # Run tests with mock data to avoid NLTK downloads
    print(f"Testing model: {model_name}")
    
    # Create mock test results instead of running actual tests
    # This avoids the TextAttack import issue
    mock_test_results = {
        "model_name": model_name,
        "model_type": model_type,
        "tests": [
            {
                "test_name": "langtest",
                "metrics": {
                    "accuracy": 0.85,
                    "robustness": 0.72,
                    "bias": 0.15,
                },
                "passed": True,
                "details": "Model performs well on general language tasks"
            },
            {
                "test_name": "deepchecks",
                "metrics": {
                    "data_integrity": 0.92,
                    "model_integrity": 0.88,
                    "concept_drift": 0.05,
                },
                "passed": True,
                "details": "Model passes all integrity checks"
            },
            {
                "test_name": "textattack",
                "metrics": {
                    "adversarial_success_rate": 0.25,
                    "average_perturbed_words": 3.2,
                    "attack_attempts": 100,
                },
                "passed": True,
                "details": "Model is reasonably robust to adversarial attacks"
            }
        ],
        "overall_score": 1.0,
    }
    
    # Save mock test results
    save_json(mock_test_results, test_output)
    print(f"Test results saved to {test_output}")
    
    # Generate roast
    try:
        roast_results = generate_model_roast(mock_test_results)
        save_json(roast_results, roast_output)
        print(f"Roast results saved to {roast_output}")
        print(f"Roast: {roast_results['combined_roast']}")
    except Exception as e:
        logger.error(f"Error generating roast: {str(e)}")
        print(f"Error generating roast: {str(e)}")
    
    # Generate meme
    try:
        meme_path = generate_model_meme(mock_test_results, meme_output)
        print(f"Meme saved to {meme_path}")
    except Exception as e:
        logger.error(f"Error generating meme: {str(e)}")
        print(f"Error generating meme: {str(e)}")
    
    print(f"✅ AI Roast Machine test completed!")


if __name__ == "__main__":
    main() 