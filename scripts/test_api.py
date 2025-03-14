#!/usr/bin/env python
"""Test script for AI Roast Machine API endpoints."""
import requests
import json
from typing import Dict, Any

def test_endpoint(url: str, method: str = "GET", data: Dict[str, Any] = None) -> None:
    """Test an API endpoint.
    
    Args:
        url: Endpoint URL
        method: HTTP method
        data: Request data (for POST)
    """
    print(f"\n🧪 Testing {method} {url}")
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        print(f"Status: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        assert response.status_code == 200, "Expected 200 status code"
        print("✅ Test passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def main():
    """Run all API tests."""
    BASE_URL = "http://localhost:8000"
    
    # Test health endpoint
    test_endpoint(f"{BASE_URL}/health")
    
    # Test model testing
    test_data = {
        "model_name": "gpt2",
        "model_type": "text-generation",
        "test_data": {
            "sample_text": "Hello, world!",
            "expected_output": "Hi there!"
        }
    }
    test_endpoint(f"{BASE_URL}/test", "POST", test_data)
    
    # Test roast generation
    roast_data = {
        "test_results": {
            "model_name": "gpt2",
            "overall_score": 0.42,
            "tests": [
                {
                    "test_name": "langtest",
                    "metrics": {
                        "accuracy": 0.65,
                        "robustness": 0.45
                    }
                }
            ]
        }
    }
    test_endpoint(f"{BASE_URL}/roast", "POST", roast_data)
    
    # Test meme generation
    test_endpoint(f"{BASE_URL}/meme", "POST", roast_data)

if __name__ == "__main__":
    main() 