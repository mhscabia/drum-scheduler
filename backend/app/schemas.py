from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserAdmin(User):
    """Extended user info for admin access only"""
    pass

# Room Schemas
class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int = 1
    equipment: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    equipment: Optional[str] = None
    is_active: Optional[bool] = None

class Room(RoomBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class Booking(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingWithDetails(Booking):
    room: Room
    
class BookingAdmin(BookingWithDetails):
    """Extended booking info for admin access only"""
    user: User

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Time Slot Schema
class TimeSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    is_available: bool
    room_id: int

# Class Schemas
class ClassBase(BaseModel):
    room_id: int
    teacher_name: str
    class_name: str
    student_name: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    notes: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    teacher_name: Optional[str] = None
    class_name: Optional[str] = None
    student_name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class Class(ClassBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ClassWithDetails(Class):
    room: Room


# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    teacher_name: str
    room_id: int
    weekday: int = Field(..., ge=0, le=6)  # 0=Mon, 1=Tue, ..., 6=Sun
    start_time: str = Field(..., pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    end_time: str = Field(..., pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    notes: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    teacher_name: Optional[str] = None
    room_id: Optional[int] = None
    weekday: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[str] = Field(
        None, pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
    )
    end_time: Optional[str] = Field(
        None, pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
    )
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class Student(StudentBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentWithDetails(Student):
    room: Room
