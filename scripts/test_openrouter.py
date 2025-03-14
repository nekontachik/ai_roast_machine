#!/usr/bin/env python
"""Simple test script for the OpenRouter connector."""
import os
import sys
import json
import time
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# Import the OpenRouter connector
from src.openrouter_connector import (
    query_model,
    get_available_models,
    extract_text_from_response,
    test_model_bias
)

def test_get_models():
    """Test getting available models."""
    print("Testing get_available_models()...")
    try:
        models = get_available_models()
        print(f"Found {len(models)} models")
        print("First 3 models:")
        for i, model in enumerate(models[:3]):
            print(f"  {i+1}. {model.get('id', 'Unknown')} - {model.get('name', 'Unknown')}")
        print("Test passed!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_query_model():
    """Test querying a model."""
    print("\nTesting query_model()...")
    try:
        model = "mistral-7b"  # Use a reliable model for testing
        prompt = "Explain what an API is in one paragraph."
        
        print(f"Querying model: {model}")
        print(f"Prompt: {prompt}")
        
        start_time = time.time()
        response = query_model(prompt, model)
        end_time = time.time()
        
        text = extract_text_from_response(response)
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {text[:200]}...")
        print("Test passed!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_bias():
    """Test bias detection."""
    print("\nTesting test_model_bias()...")
    try:
        model = "mistral-7b"  # Use a reliable model for testing
        
        print(f"Testing model: {model} for bias")
        
        start_time = time.time()
        results = test_model_bias(model, max_prompts=2)  # Use only 2 prompts for quick testing
        end_time = time.time()
        
        print(f"Test time: {end_time - start_time:.2f} seconds")
        print(f"Bias score: {results['bias_score']:.2f}")
        print(f"Potentially biased responses: {results['potentially_biased_responses']} out of {len(results['prompts'])}")
        print("Test passed!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=== OpenRouter Connector Tests ===\n")
    
    # Check if API key is set
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("Please set it in your .env file or environment")
        return False
    
    # Run tests
    tests = [
        test_get_models,
        test_query_model,
        test_bias
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {results.count(True)}")
    print(f"Failed: {results.count(False)}")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 