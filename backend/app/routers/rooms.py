from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..auth import get_current_active_user
from ..models import User
from ..schemas import Room, RoomCreate, RoomUpdate
from ..crud import get_rooms, get_room, create_room, update_room

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/", response_model=List[Room])
def read_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all available rooms"""
    rooms = get_rooms(db, skip=skip, limit=limit)
    return rooms

@router.get("/{room_id}", response_model=Room)
def read_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific room"""
    db_room = get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
