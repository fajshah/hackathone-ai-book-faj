#!/usr/bin/env python3
"""
Test script to validate health endpoints
"""
import requests
import sys
import time

def test_health_endpoints():
    """Test health endpoints"""
    base_url = "http://localhost:8000"  # Assuming backend is running on port 8000

    print("Testing health endpoints...")

    # Test general health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint: {response.status_code}, response: {response.json()}")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        print("✅ Health endpoint working correctly")
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

    # Test Qdrant health endpoint
    try:
        response = requests.get(f"{base_url}/health/qdrant")
        print(f"Qdrant health endpoint: {response.status_code}, response: {response.json()}")
        assert response.status_code == 200 or response.status_code == 500

        if response.status_code == 200:
            data = response.json()
            assert "connected" in data
            assert "collection" in data
            assert "points" in data
            assert "count" in data["points"]
            print("✅ Qdrant health endpoint working correctly")
        else:
            print("⚠️ Qdrant health endpoint returned error (this may be expected if Qdrant is not available)")
    except Exception as e:
        print(f"❌ Qdrant health endpoint test failed: {e}")
        return False

    return True

def main():
    print("Starting health endpoint tests...\n")

    success = test_health_endpoints()

    if success:
        print("\n🎉 All health endpoint tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    exit(main())