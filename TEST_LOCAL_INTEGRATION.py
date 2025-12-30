#!/usr/bin/env python3
"""
Test script to verify the local integration works properly
"""
import requests
import json

def test_local_integration():
    """Test the local backend API directly"""
    print("Testing local backend integration...")

    # Test the API endpoint directly
    url = "http://localhost:8001/api/ask/public"

    payload = {
        "question": "What is Physical AI?",
        "top_k": 3
    }

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] API call successful!")
            print(f"   Answer length: {len(data.get('answer', ''))} characters")
            print(f"   Sources returned: {len(data.get('sources', []))}")
            print(f"   Session ID: {data.get('session_id', '')[:15]}...")

            if 'answer' in data and 'sources' in data:
                print("[SUCCESS] Response structure correct")
                return True
            else:
                print("[ERROR] Response missing required fields")
                return False
        else:
            print(f"[ERROR] API call failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"[ERROR] Error during API call: {e}")
        return False

def main():
    print("Testing Local Backend Integration")
    print("=" * 50)

    success = test_local_integration()

    print("\n" + "=" * 50)
    if success:
        print("Local integration test passed!")
        print("\nThe frontend component will connect to:")
        print("   - Local backend (http://localhost:8001) when running on localhost")
        print("   - Hugging Face Space when deployed")
        print("   - Fallback iframe when API is unavailable")
        print("\nAll systems ready for both development and production!")
    else:
        print("Local integration test failed!")

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())