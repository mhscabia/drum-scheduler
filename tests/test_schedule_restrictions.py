#!/usr/bin/env python3
"""
Test script to verify the new schedule restrictions:
1. No bookings on Sunday
2. Saturday bookings only until 1 PM
"""

import requests
import json
from datetime import datetime, timedelta

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
        print(response.text)
        return None

def get_available_slots(token, room_id, date_str):
    """Get available slots for a specific date"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{BASE_URL}/bookings/available-slots",
        params={"room_id": room_id, "date": date_str},
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get slots for {date_str}: {response.status_code}")
        print(response.text)
        return []

def get_rooms(token):
    """Get list of rooms"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/rooms/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get rooms: {response.status_code}")
        return []

def test_schedule_restrictions():
    """Test the new schedule restrictions"""
    print("🧪 Testing Schedule Restrictions")
    print("=" * 50)
    
    # Get admin token
    token = get_admin_token()
    if not token:
        print("❌ Failed to authenticate")
        return
    
    print("✅ Admin authentication successful")
    
    # Get rooms
    rooms = get_rooms(token)
    if not rooms:
        print("❌ No rooms found or failed to fetch rooms")
        return
    
    room_id = rooms[0]["id"]
    room_name = rooms[0]["name"]
    print(f"✅ Using room: {room_name} (ID: {room_id})")
    
    # Calculate test dates
    today = datetime.now()
    
    # Find next Sunday
    days_until_sunday = (6 - today.weekday()) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    next_sunday = today + timedelta(days=days_until_sunday)
    
    # Find next Saturday
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7
    next_saturday = today + timedelta(days=days_until_saturday)
    
    # Find next Monday
    days_until_monday = (0 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    next_monday = today + timedelta(days=days_until_monday)
    
    print("\n🗓️ Testing dates:")
    print(f"  • Sunday: {next_sunday.strftime('%Y-%m-%d (%A)')}")
    print(f"  • Saturday: {next_saturday.strftime('%Y-%m-%d (%A)')}")
    print(f"  • Monday: {next_monday.strftime('%Y-%m-%d (%A)')}")
    
    # Test Sunday (should have NO slots)
    print(f"\n📅 Testing Sunday ({next_sunday.strftime('%Y-%m-%d')}):")
    sunday_slots = get_available_slots(token, room_id, next_sunday.strftime('%Y-%m-%d'))
    if len(sunday_slots) == 0:
        print("  ✅ PASS: Sunday has no available slots (school closed)")
    else:
        print(f"  ❌ FAIL: Sunday has {len(sunday_slots)} slots (should be 0)")
        print(f"       First slot: {sunday_slots[0]['start_time'] if sunday_slots else 'N/A'}")
    
    # Test Saturday (should only have slots until 1 PM)
    print(f"\n📅 Testing Saturday ({next_saturday.strftime('%Y-%m-%d')}):")
    saturday_slots = get_available_slots(token, room_id, next_saturday.strftime('%Y-%m-%d'))
    
    if len(saturday_slots) > 0:
        # Check if any slot starts at or after 1 PM (13:00)
        late_slots = []
        for slot in saturday_slots:
            slot_time = datetime.fromisoformat(slot['start_time'].replace('Z', '+00:00'))
            if slot_time.hour >= 13:
                late_slots.append(slot)
        
        if len(late_slots) == 0:
            print(f"  ✅ PASS: Saturday has {len(saturday_slots)} slots, all before 1 PM")
            if saturday_slots:
                last_slot = saturday_slots[-1]
                last_time = datetime.fromisoformat(last_slot['start_time'].replace('Z', '+00:00'))
                print(f"       Last slot starts at: {last_time.strftime('%H:%M')}")
        else:
            print(f"  ❌ FAIL: Saturday has {len(late_slots)} slots at/after 1 PM")
            for slot in late_slots[:3]:  # Show first 3
                slot_time = datetime.fromisoformat(slot['start_time'].replace('Z', '+00:00'))
                print(f"       Invalid slot at: {slot_time.strftime('%H:%M')}")
    else:
        print("  ⚠️  WARNING: Saturday has no slots at all")
    
    # Test Monday (should have normal slots 9 AM - 9 PM)
    print(f"\n📅 Testing Monday ({next_monday.strftime('%Y-%m-%d')}):")
    monday_slots = get_available_slots(token, room_id, next_monday.strftime('%Y-%m-%d'))
    
    if len(monday_slots) > 0:
        first_slot = datetime.fromisoformat(monday_slots[0]['start_time'].replace('Z', '+00:00'))
        last_slot = datetime.fromisoformat(monday_slots[-1]['start_time'].replace('Z', '+00:00'))
        
        expected_first_hour = 9  # 9 AM
        expected_last_hour = 20  # 8 PM (last slot that ends by 9 PM)
        
        if first_slot.hour == expected_first_hour and last_slot.hour <= expected_last_hour:
            print(f"  ✅ PASS: Monday has {len(monday_slots)} slots from {first_slot.strftime('%H:%M')} to {last_slot.strftime('%H:%M')}")
        else:
            print(f"  ❌ FAIL: Monday schedule incorrect")
            print(f"       First slot: {first_slot.strftime('%H:%M')} (expected: 09:00)")
            print(f"       Last slot: {last_slot.strftime('%H:%M')} (expected: ≤20:00)")
    else:
        print("  ❌ FAIL: Monday has no slots")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_schedule_restrictions()
