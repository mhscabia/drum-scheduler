from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    bookings = relationship("Booking", back_populates="user")

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    capacity = Column(Integer, default=1)
    equipment = Column(Text)  # JSON string of available equipment
    is_active = Column(Boolean, default=True)
    
    # Relationships
    bookings = relationship("Booking", back_populates="room")
    classes = relationship("Class", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    notes = Column(Text)
    status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    teacher_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    student_name = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String)  # weekly, monthly, etc.
    notes = Column(Text)
    status = Column(String, default="scheduled")  # scheduled, cancelled, completed
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    room = relationship("Room", back_populates="classes")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    teacher_name = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    weekday = Column(Integer, nullable=False)  # 0=Mon, 1=Tue, ..., 6=Sun
    start_time = Column(String, nullable=False)  # Format: "14:00"
    end_time = Column(String, nullable=False)    # Format: "15:00"
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    room = relationship("Room")
