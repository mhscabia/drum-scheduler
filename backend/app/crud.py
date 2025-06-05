from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import Optional

from . import models, schemas
from .auth import get_password_hash

# User CRUD operations


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Room CRUD operations
def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    query = db.query(models.Room)
    if active_only:
        query = query.filter(models.Room.is_active == True)
    return query.offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room(db: Session, room_id: int, room_update: schemas.RoomUpdate):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        update_data = room_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_room, field, value)
        db.commit()
        db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        # Instead of hard delete, mark as inactive
        db_room.is_active = False
        db.commit()
        return True
    return False

# Booking CRUD operations
def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_user_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).filter(
        models.Booking.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    # Check for conflicts
    conflicts = db.query(models.Booking).filter(
        and_(
            models.Booking.room_id == booking.room_id,
            models.Booking.status == "confirmed",
            or_(
                and_(
                    models.Booking.start_time <= booking.start_time,
                    models.Booking.end_time > booking.start_time
                ),
                and_(
                    models.Booking.start_time < booking.end_time,
                    models.Booking.end_time >= booking.end_time
                ),
                and_(
                    models.Booking.start_time >= booking.start_time,
                    models.Booking.end_time <= booking.end_time
                )
            )
        )
    ).first()
    
    if conflicts:
        return None  # Conflict found
    
    db_booking = models.Booking(
        **booking.dict(),
        user_id=user_id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(db: Session, booking_id: int, booking_update: schemas.BookingUpdate):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        update_data = booking_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_booking, field, value)
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return True
    return False

def get_available_slots(db: Session, room_id: int, date: datetime, duration_minutes: int = 60):
    """Get available time slots for a specific room and date"""
    
    # Check if it's Sunday (weekday 6) or Friday (weekday 4) - no availability on these days
    if date.weekday() == 6 or date.weekday() == 4:  # Sunday or Friday
        return []
    
    # Define business hours based on day of week
    start_of_day = date.replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Saturday closes at 1 PM (13:00), other days at 9 PM (21:00)
    if date.weekday() == 5:  # Saturday
        end_of_day = date.replace(hour=13, minute=0, second=0, microsecond=0)
    else:  # Monday to Thursday
        end_of_day = date.replace(hour=21, minute=0, second=0, microsecond=0)
    
    # Get existing bookings for the day
    existing_bookings = db.query(models.Booking).filter(
        and_(
            models.Booking.room_id == room_id,
            models.Booking.start_time >= start_of_day,
            models.Booking.start_time < end_of_day + timedelta(days=1),
            models.Booking.status == "confirmed"
        )
    ).order_by(models.Booking.start_time).all()
    
    # Generate available slots
    available_slots = []
    current_time = start_of_day
    slot_duration = timedelta(minutes=duration_minutes)
    
    while current_time + slot_duration <= end_of_day:
        slot_end = current_time + slot_duration
        
        # Check if this slot conflicts with any booking
        is_available = True
        for booking in existing_bookings:
            if (current_time < booking.end_time and slot_end > booking.start_time):
                is_available = False
                break
        
        available_slots.append(schemas.TimeSlot(
            start_time=current_time,
            end_time=slot_end,
            is_available=is_available,
            room_id=room_id
        ))
        
        current_time += slot_duration
    
    return available_slots

# Class CRUD operations
def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()

def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Class).offset(skip).limit(limit).all()

def get_classes_by_room(db: Session, room_id: int, start_date: datetime = None, end_date: datetime = None):
    query = db.query(models.Class).filter(models.Class.room_id == room_id)
    if start_date:
        query = query.filter(models.Class.start_time >= start_date)
    if end_date:
        query = query.filter(models.Class.end_time <= end_date)
    return query.order_by(models.Class.start_time).all()

def create_class(db: Session, class_data: schemas.ClassCreate):
    # Check for conflicts with existing bookings and classes
    conflicts = db.query(models.Booking).filter(
        and_(
            models.Booking.room_id == class_data.room_id,
            models.Booking.status == "confirmed",
            or_(
                and_(
                    models.Booking.start_time <= class_data.start_time,
                    models.Booking.end_time > class_data.start_time
                ),
                and_(
                    models.Booking.start_time < class_data.end_time,
                    models.Booking.end_time >= class_data.end_time
                ),
                and_(
                    models.Booking.start_time >= class_data.start_time,
                    models.Booking.end_time <= class_data.end_time
                )
            )
        )
    ).first()
    
    if conflicts:
        return None  # Conflict with booking found
    
    # Check for conflicts with existing classes
    class_conflicts = db.query(models.Class).filter(
        and_(
            models.Class.room_id == class_data.room_id,
            models.Class.status == "scheduled",
            or_(
                and_(
                    models.Class.start_time <= class_data.start_time,
                    models.Class.end_time > class_data.start_time
                ),
                and_(
                    models.Class.start_time < class_data.end_time,
                    models.Class.end_time >= class_data.end_time
                ),
                and_(
                    models.Class.start_time >= class_data.start_time,
                    models.Class.end_time <= class_data.end_time
                )
            )
        )
    ).first()
    
    if class_conflicts:
        return None  # Conflict with another class found
    
    db_class = models.Class(**class_data.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def update_class(db: Session, class_id: int, class_update: schemas.ClassUpdate):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if db_class:
        update_data = class_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_class, field, value)
        db.commit()
        db.refresh(db_class)
    return db_class

def delete_class(db: Session, class_id: int):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if db_class:
        db.delete(db_class)
        db.commit()
        return True
    return False

def get_available_slots_with_classes(db: Session, room_id: int, date: datetime, duration_minutes: int = 60):
    """Get available time slots for a specific room and date, considering both bookings and classes"""
    
    # Check if it's Sunday (weekday 6) or Friday (weekday 4) - no availability on these days
    if date.weekday() == 6 or date.weekday() == 4:  # Sunday or Friday
        return []
    
    # Define business hours based on day of week
    start_of_day = date.replace(hour=9, minute=0, second=0, microsecond=0)
      # Saturday closes at 1 PM (13:00), other days at 9 PM (21:00)
    if date.weekday() == 5:  # Saturday
        end_of_day = date.replace(hour=13, minute=0, second=0, microsecond=0)
    else:  # Monday to Thursday
        end_of_day = date.replace(hour=21, minute=0, second=0, microsecond=0)
    
    # Get existing bookings for the day
    existing_bookings = db.query(models.Booking).filter(
        and_(
            models.Booking.room_id == room_id,
            models.Booking.start_time >= start_of_day,
            models.Booking.start_time < end_of_day + timedelta(days=1),
            models.Booking.status == "confirmed"
        )
    ).order_by(models.Booking.start_time).all()
      # Get existing classes for the day
    existing_classes = db.query(models.Class).filter(
        and_(
            models.Class.room_id == room_id,
            models.Class.start_time >= start_of_day,
            models.Class.start_time < end_of_day + timedelta(days=1),
            models.Class.status == "scheduled"
        )
    ).order_by(models.Class.start_time).all()
    
    # Get student schedules for this day of week
    student_schedules = db.query(models.Student).filter(
        and_(
            models.Student.room_id == room_id,
            models.Student.weekday == date.weekday(),
            models.Student.is_active.is_(True)
        )
    ).all()
    
    # Generate available slots
    available_slots = []
    current_time = start_of_day
    slot_duration = timedelta(minutes=duration_minutes)
    
    while current_time + slot_duration <= end_of_day:
        slot_end = current_time + slot_duration
        
        # Check if this slot conflicts with any booking
        is_available = True
        for booking in existing_bookings:
            if (current_time < booking.end_time and slot_end > booking.start_time):
                is_available = False
                break
          # Check if this slot conflicts with any class
        if is_available:
            for class_schedule in existing_classes:
                if (current_time < class_schedule.end_time and 
                    slot_end > class_schedule.start_time):
                    is_available = False
                    break
        
        # Check if this slot conflicts with any student schedule
        if is_available:
            for student in student_schedules:
                # Convert student time strings to datetime objects
                student_start_hour, student_start_min = map(
                    int, student.start_time.split(':')
                )
                student_end_hour, student_end_min = map(
                    int, student.end_time.split(':')
                )
                
                student_start = date.replace(
                    hour=student_start_hour, 
                    minute=student_start_min,
                    second=0, 
                    microsecond=0
                )
                student_end = date.replace(
                    hour=student_end_hour,
                    minute=student_end_min,
                    second=0,
                    microsecond=0
                )
                
                if (current_time < student_end and slot_end > student_start):
                    is_available = False
                    break
        
        available_slots.append(schemas.TimeSlot(
            start_time=current_time,
            end_time=slot_end,
            is_available=is_available,
            room_id=room_id
        ))
        
        current_time += slot_duration
    
    return available_slots

# Student CRUD operations
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).filter(
        models.Student.is_active.is_(True)
    ).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_active.is_(True)
    ).first()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, 
                   student_update: schemas.StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    
    update_data = student_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    
    # Soft delete
    db_student.is_active = False
    db.commit()
    return db_student


def get_students_by_room(db: Session, room_id: int):
    return db.query(models.Student).filter(
        models.Student.room_id == room_id,
        models.Student.is_active.is_(True)
    ).all()
