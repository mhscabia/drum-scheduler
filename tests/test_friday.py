#!/usr/bin/env python3
"""
Simple test to verify Friday restriction
"""

import requests
import json

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@drumschool.com"
ADMIN_PASSWORD = "admin123"

def get_admin_token():
    """Authenticate and get admin token"""
    login_data = {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        return None

def test_friday_restriction():
    """Test that Friday has no available slots"""
    print("Testing Friday restriction...")
    
    token = get_admin_token()
    if not token:
        print("Failed to get admin token")
        return
    
    print("Got admin token successfully")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test Friday 2025-06-06
    friday_date = "2025-06-06"
    
    response = requests.get(
        f"{BASE_URL}/bookings/available-slots",
        params={"room_id": 1, "date": friday_date},
        headers=headers
    )
    
    if response.status_code == 200:
        slots = response.json()
        print(f"Friday {friday_date} available slots: {len(slots)}")
        if len(slots) == 0:
            print("✓ Friday restriction working - no slots available")
        else:
            print("✗ Friday restriction failed - slots still available:")
            for slot in slots:
                print(f"  - {slot}")
    else:
        print(f"Failed to get slots: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_friday_restriction()
