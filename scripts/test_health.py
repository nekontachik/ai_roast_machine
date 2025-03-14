#!/usr/bin/env python
"""Simple health check for the API."""
import requests
import time
import sys

def check_health(url, max_retries=10, retry_delay=3):
    """Check if the API is healthy.
    
    Args:
        url: Health check URL
        max_retries: Maximum number of retries
        retry_delay: Delay between retries in seconds
        
    Returns:
        True if healthy, False otherwise
    """
    for i in range(max_retries):
        try:
            print(f"Attempt {i+1}/{max_retries}: Checking {url}...")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ API is healthy! Response: {response.json()}")
                return True
            else:
                print(f"❌ API returned status code {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ Connection error: {e}")
        
        if i < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    return False

if __name__ == "__main__":
    url = "http://localhost:8000/health"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    if check_health(url):
        sys.exit(0)
    else:
        print("❌ Health check failed after maximum retries")
        sys.exit(1) 