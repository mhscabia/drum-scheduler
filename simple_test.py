#!/usr/bin/env python3
"""
Simple test for student functionality
"""

import requests
import sys

def test_connection():
    try:
        # Test basic connection
        print("Testing backend connection...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test auth endpoint
        print("\nTesting auth...")
        login_data = {"email": "admin@example.com", "password": "admin123"}
        auth_response = requests.post("http://localhost:8000/auth/login", json=login_data, timeout=5)
        print(f"Auth response: {auth_response.status_code}")
        
        if auth_response.status_code == 200:
            token = auth_response.json()["access_token"]
            print("✅ Successfully authenticated")
            
            # Test students endpoint
            headers = {"Authorization": f"Bearer {token}"}
            students_response = requests.get("http://localhost:8000/students/", headers=headers, timeout=5)
            print(f"Students endpoint: {students_response.status_code}")
            if students_response.status_code == 200:
                print("✅ Students API is accessible")
                students = students_response.json()
                print(f"Current students: {len(students)}")
                return True
            else:
                print(f"❌ Students API error: {students_response.text}")
                return False
        else:
            print(f"❌ Auth failed: {auth_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        print("\n🎉 Basic student API test passed!")
    else:
        print("\n❌ Test failed.")
        sys.exit(1)
