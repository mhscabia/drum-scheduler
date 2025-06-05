from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date, timedelta

from ..database import get_db
from ..auth import get_current_active_user
from ..models import User
from ..schemas import Booking, BookingCreate, BookingUpdate, BookingWithDetails, TimeSlot
from ..crud import (
    get_user_bookings,
    create_booking,
    update_booking,
    delete_booking,
    get_booking,
    get_available_slots_with_classes
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/my-bookings", response_model=List[BookingWithDetails])
def read_my_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's bookings"""
    bookings = get_user_bookings(db, user_id=current_user.id, skip=skip, limit=limit)
    return bookings

@router.post("/", response_model=Booking)
def create_booking_endpoint(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new booking"""
    # Validate booking time
    if booking.start_time >= booking.end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )    # Allow booking slots that start at least 15 minutes from now
    # Use local time to match frontend timezone
    current_time_with_buffer = datetime.now() + timedelta(minutes=15)
    if booking.start_time < current_time_with_buffer:
        raise HTTPException(
            status_code=400,
            detail="Não é possível agendar horários no passado"
        )
    
    db_booking = create_booking(db=db, booking=booking, user_id=current_user.id)
    if db_booking is None:
        raise HTTPException(
            status_code=409,
            detail="Time slot is already booked"
        )
    return db_booking

@router.put("/{booking_id}", response_model=Booking)
def update_booking_endpoint(
    booking_id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a booking (only owner can update)"""
    db_booking = get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if db_booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    updated_booking = update_booking(db=db, booking_id=booking_id, booking_update=booking_update)
    return updated_booking

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancel a booking (only owner can cancel)"""
    db_booking = get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if db_booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    
    success = delete_booking(db=db, booking_id=booking_id)
    if success:
        return {"message": "Booking cancelled successfully"}
    else:
        raise HTTPException(status_code=404, detail="Booking not found")

@router.get("/available-slots", response_model=List[TimeSlot])
def get_available_time_slots(
    room_id: int,
    date: date = Query(..., description="Date to check availability (YYYY-MM-DD)"),
    duration: int = Query(60, description="Duration in minutes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get available time slots for a specific room and date"""
    date_datetime = datetime.combine(date, datetime.min.time())
    slots = get_available_slots_with_classes(db, room_id=room_id, date=date_datetime, duration_minutes=duration)
    return slots
