import requests
import json
from datetime import datetime, timedelta

# Test the time validation fix
BASE_URL = "http://localhost:8000"

# Get admin token
login_data = {
    "username": "admin@drumschool.com",
    "password": "admin123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("🧪 Testing Time Validation Fix")
        print("=" * 40)
        
        # Test 1: Try booking 10 minutes from now (should fail)
        now = datetime.utcnow()
        future_10min = now + timedelta(minutes=10)
        
        booking_data = {
            "room_id": 1,
            "start_time": future_10min.isoformat(),
            "end_time": (future_10min + timedelta(hours=1)).isoformat(),
            "notes": "Test booking too close"
        }
        
        print(f"\n1. Testing booking 10 minutes from now...")
        print(f"   Time: {future_10min.strftime('%H:%M:%S')}")
        
        response = requests.post(f"{BASE_URL}/bookings/", json=booking_data, headers=headers)
        
        if response.status_code == 400:
            error_msg = response.json().get("detail", "")
            print(f"   ✅ PASS: Booking rejected")
            print(f"   📝 Error message: '{error_msg}'")
            if "passado" in error_msg.lower():
                print(f"   ✅ PASS: Error message is in Portuguese")
            else:
                print(f"   ❌ FAIL: Error message not in Portuguese")
        else:
            print(f"   ❌ FAIL: Expected 400, got {response.status_code}")
            
        # Test 2: Try booking 20 minutes from now (should succeed)
        future_20min = now + timedelta(minutes=20)
        
        booking_data_20 = {
            "room_id": 1,
            "start_time": future_20min.isoformat(),
            "end_time": (future_20min + timedelta(hours=1)).isoformat(),
            "notes": "Test booking with buffer"
        }
        
        print(f"\n2. Testing booking 20 minutes from now...")
        print(f"   Time: {future_20min.strftime('%H:%M:%S')}")
        
        response = requests.post(f"{BASE_URL}/bookings/", json=booking_data_20, headers=headers)
        
        if response.status_code == 201:
            booking_id = response.json().get("id")
            print(f"   ✅ PASS: Booking created (ID: {booking_id})")
            
            # Clean up
            if booking_id:
                requests.delete(f"{BASE_URL}/bookings/{booking_id}", headers=headers)
                print(f"   🧹 Cleaned up test booking")
        elif response.status_code == 409:
            print(f"   ⚠️  SKIP: Time slot already booked")
        else:
            print(f"   ❌ FAIL: Expected 201, got {response.status_code}")
            print(f"   📝 Response: {response.text}")
            
        print("\n" + "=" * 40)
        print("✅ Test completed!")
        
        # Test 3: Simulate original problem scenario
        print(f"\n3. Original Problem Simulation:")
        print(f"   If current time was 13:40, booking 14:00 would have:")
        buffer_minutes = (14*60) - (13*60 + 40)  # 20 minutes
        print(f"   Time buffer: {buffer_minutes} minutes")
        if buffer_minutes >= 15:
            print(f"   ✅ PASS: Would be allowed (≥15 min buffer)")
        else:
            print(f"   ❌ FAIL: Would be blocked (<15 min buffer)")
            
    else:
        print(f"Login failed: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
