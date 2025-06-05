import requests
import json
from datetime import datetime, timedelta

# Test the timezone fix by attempting the same booking that was failing
BASE_URL = "http://localhost:8000"

def test_timezone_fix():
    try:
        # Test server connectivity first
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server not responding")
            return
        
        print("✅ Backend server is running")
        
        # Login as admin
        login_data = {
            "username": "admin@drumschool.com", 
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            print("❌ Login failed")
            return
            
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful")
        
        # Test the specific case: trying to book 15:00-16:00 slot
        # when current time is around 14:xx
        now = datetime.now()
        print(f"📅 Current local time: {now.strftime('%H:%M:%S')}")
        
        # Try to book a slot for 15:00 today
        booking_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        end_time = booking_time.replace(hour=16)
        
        # If it's already past 15:00, use tomorrow
        if now.hour >= 15:
            booking_time = booking_time + timedelta(days=1)
            end_time = end_time + timedelta(days=1)
            print(f"⏰ Using tomorrow's date since it's past 15:00")
        
        time_diff = (booking_time - now).total_seconds() / 60
        print(f"⏱️  Time difference: {time_diff:.1f} minutes from now")
        
        booking_data = {
            "room_id": 1,
            "start_time": booking_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "notes": "Test timezone fix"
        }
        
        print(f"🎯 Attempting to book: {booking_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}")
        
        response = requests.post(f"{BASE_URL}/bookings/", json=booking_data, headers=headers)
        
        if response.status_code == 201:
            booking_id = response.json().get("id")
            print("✅ SUCCESS: Booking created successfully!")
            print(f"📝 Booking ID: {booking_id}")
            
            # Clean up the test booking
            if booking_id:
                cleanup_response = requests.delete(f"{BASE_URL}/bookings/{booking_id}", headers=headers)
                if cleanup_response.status_code == 200:
                    print("🧹 Test booking cleaned up")
                    
        elif response.status_code == 400:
            error_detail = response.json().get("detail", "")
            print(f"❌ FAILED: {error_detail}")
            if time_diff >= 15:
                print("🐛 This should have succeeded - timezone issue still exists!")
            else:
                print("✅ This failure is expected (less than 15 min buffer)")
                
        elif response.status_code == 409:
            print("⚠️  CONFLICT: Time slot already booked (this is normal)")
            
        else:
            print(f"❌ UNEXPECTED: Status {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Timezone Fix for 15:00 Booking Issue")
    print("=" * 50)
    test_timezone_fix()
    print("=" * 50)
