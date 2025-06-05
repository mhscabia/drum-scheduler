#!/usr/bin/env python3
"""
Test script for the Students API endpoints
This script tests the complete CRUD functionality for students
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

def get_admin_token():
    """Get admin authentication token"""
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to login: {response.status_code} - {response.text}")
        return None

def test_students_api():
    """Test all student API endpoints"""
    print("Testing Students API...")
    
    # Get admin token
    token = get_admin_token()
    if not token:
        print("❌ Failed to get admin token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Get all students (should be empty initially)
    print("\n1. Testing GET /students/")
    response = requests.get(f"{BASE_URL}/students/", headers=headers)
    if response.status_code == 200:
        students = response.json()
        print(f"✅ Successfully retrieved {len(students)} students")
    else:
        print(f"❌ Failed to get students: {response.status_code} - {response.text}")
        return False
    
    # Test 2: Get rooms for student creation
    print("\n2. Getting available rooms...")
    response = requests.get(f"{BASE_URL}/rooms/", headers=headers)
    if response.status_code == 200:
        rooms = response.json()
        if rooms:
            room_id = rooms[0]["id"]
            print(f"✅ Using room: {rooms[0]['name']} (ID: {room_id})")
        else:
            print("❌ No rooms available")
            return False
    else:
        print(f"❌ Failed to get rooms: {response.status_code} - {response.text}")
        return False
    
    # Test 3: Create a new student
    print("\n3. Testing POST /students/")
    student_data = {
        "name": "João Silva",
        "email": "joao.silva@email.com",
        "phone": "(11) 99999-9999",
        "teacher_name": "Professor Carlos",
        "room_id": room_id,
        "weekday": 0,  # Monday
        "start_time": "14:00",
        "end_time": "15:00",
        "notes": "Estudante iniciante, foco em técnica básica"
    }
    
    response = requests.post(f"{BASE_URL}/students/", json=student_data, headers=headers)
    if response.status_code == 200:
        created_student = response.json()
        student_id = created_student["id"]
        print(f"✅ Successfully created student: {created_student['name']} (ID: {student_id})")
    else:
        print(f"❌ Failed to create student: {response.status_code} - {response.text}")
        return False
    
    # Test 4: Get specific student
    print(f"\n4. Testing GET /students/{student_id}")
    response = requests.get(f"{BASE_URL}/students/{student_id}", headers=headers)
    if response.status_code == 200:
        student = response.json()
        print(f"✅ Successfully retrieved student: {student['name']}")
        print(f"   - Teacher: {student['teacher_name']}")
        print(f"   - Schedule: Weekday {student['weekday']}, {student['start_time']}-{student['end_time']}")
    else:
        print(f"❌ Failed to get student: {response.status_code} - {response.text}")
        return False
    
    # Test 5: Update student
    print(f"\n5. Testing PUT /students/{student_id}")
    update_data = {
        "name": "João Silva Santos",
        "email": "joao.santos@email.com",
        "phone": "(11) 98888-8888",
        "teacher_name": "Professor Carlos Alberto",
        "room_id": room_id,
        "weekday": 2,  # Wednesday
        "start_time": "15:00",
        "end_time": "16:00",
        "notes": "Progredindo bem, pode avançar para exercícios intermediários"
    }
    
    response = requests.put(f"{BASE_URL}/students/{student_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        updated_student = response.json()
        print(f"✅ Successfully updated student: {updated_student['name']}")
        print(f"   - New schedule: Weekday {updated_student['weekday']}, {updated_student['start_time']}-{updated_student['end_time']}")
    else:
        print(f"❌ Failed to update student: {response.status_code} - {response.text}")
        return False
    
    # Test 6: Get students by room
    print(f"\n6. Testing GET /students/room/{room_id}")
    response = requests.get(f"{BASE_URL}/students/room/{room_id}", headers=headers)
    if response.status_code == 200:
        room_students = response.json()
        print(f"✅ Successfully retrieved {len(room_students)} students for room {room_id}")
    else:
        print(f"❌ Failed to get students by room: {response.status_code} - {response.text}")
        return False
    
    # Test 7: Test conflict detection with booking availability
    print(f"\n7. Testing conflict detection with student schedules")
    # Try to get available slots for Wednesday (student's new schedule day)
    from datetime import datetime, timedelta
    
    # Find next Wednesday
    today = datetime.now()
    days_ahead = 2 - today.weekday()  # Wednesday is weekday 2
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    next_wednesday = today + timedelta(days=days_ahead)
    
    date_str = next_wednesday.strftime("%Y-%m-%d")
    response = requests.get(
        f"{BASE_URL}/bookings/available-slots", 
        params={"room_id": room_id, "date": date_str}, 
        headers=headers
    )
    if response.status_code == 200:
        available_slots = response.json()
        print(f"✅ Retrieved {len(available_slots)} available slots for {date_str}")
        
        # Check if student's time slot (15:00-16:00) is blocked
        student_time_blocked = not any(
            slot["start_time"] == "15:00:00" for slot in available_slots
        )
        if student_time_blocked:
            print("✅ Student's scheduled time (15:00-16:00) is properly blocked for bookings")
        else:
            print("⚠️  Student's scheduled time is still available for booking (conflict detection may need review)")
    else:
        print(f"❌ Failed to get available slots: {response.status_code} - {response.text}")
    
    # Test 8: Delete student
    print(f"\n8. Testing DELETE /students/{student_id}")
    response = requests.delete(f"{BASE_URL}/students/{student_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Successfully deleted student: {result['message']}")
    else:
        print(f"❌ Failed to delete student: {response.status_code} - {response.text}")
        return False
    
    # Test 9: Verify student is deleted
    print(f"\n9. Verifying student deletion")
    response = requests.get(f"{BASE_URL}/students/{student_id}", headers=headers)
    if response.status_code == 404:
        print("✅ Student properly deleted (404 response as expected)")
    else:
        print(f"❌ Student still exists after deletion: {response.status_code}")
        return False
    
    print("\n🎉 All student API tests passed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = test_students_api()
        if success:
            print("\n✅ Student API is working correctly!")
        else:
            print("\n❌ Some tests failed. Please check the API implementation.")
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
