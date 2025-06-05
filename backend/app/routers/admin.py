from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..auth import get_admin_user
from ..models import User
from ..schemas import (
    User as UserSchema, 
    UserAdmin, 
    UserUpdate,
    Room, 
    RoomCreate, 
    RoomUpdate,
    BookingAdmin
)
from ..crud import (
    get_users, 
    get_user, 
    update_user,
    get_rooms,
    create_room,
    update_room,
    get_bookings,
    delete_room
)

router = APIRouter(prefix="/admin", tags=["admin"])

# User management
@router.get("/users", response_model=List[UserAdmin])
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Get all users (admin only)"""
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserAdmin)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Get a specific user (admin only)"""
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserAdmin)
def update_user_admin(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Update a user (admin only)"""
    db_user = update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Room management
@router.post("/rooms", response_model=Room)
def create_room_admin(
    room: RoomCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Create a new room (admin only)"""
    return create_room(db=db, room=room)

@router.put("/rooms/{room_id}", response_model=Room)
def update_room_admin(
    room_id: int,
    room_update: RoomUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Update a room (admin only)"""
    db_room = update_room(db=db, room_id=room_id, room_update=room_update)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.get("/rooms", response_model=List[Room])
def read_all_rooms_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Get all rooms including inactive ones (admin only)"""
    rooms = get_rooms(db, skip=skip, limit=limit, active_only=False)
    return rooms

@router.delete("/rooms/{room_id}")
def delete_room_admin(
    room_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Delete a room (admin only)"""
    success = delete_room(db=db, room_id=room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}

# Booking management
@router.get("/bookings", response_model=List[BookingAdmin])
def read_all_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Get all bookings with user details (admin only)"""
    bookings = get_bookings(db, skip=skip, limit=limit)
    return bookings
