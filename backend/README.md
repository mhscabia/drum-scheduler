# Drum School Scheduling Application - Backend

FastAPI backend for the drum school practice session scheduling system.

## Features

- User registration and authentication with JWT tokens
- Role-based access control (admin and regular users)
- Room management
- Time slot booking with conflict prevention
- Admin panel for managing users, rooms, and bookings
- RESTful API with automatic documentation

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy environment file and configure:

```bash
cp .env.example .env
```

3. Run the development server:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Admin Account

- Email: admin@drumschool.com
- Password: admin123

**Important:** Change the admin password in production!

## Database

The application uses SQLite by default for development. For production, configure PostgreSQL in the `.env` file.

## API Endpoints

### Authentication

- POST `/auth/register` - Register new user
- POST `/auth/login` - Login and get access token
- GET `/auth/me` - Get current user info

### Rooms

- GET `/rooms/` - List all active rooms
- GET `/rooms/{id}` - Get room details

### Bookings

- GET `/bookings/my-bookings` - Get user's bookings
- POST `/bookings/` - Create new booking
- PUT `/bookings/{id}` - Update booking
- DELETE `/bookings/{id}` - Cancel booking
- GET `/bookings/available-slots` - Get available time slots

### Admin (Admin only)

- GET `/admin/users` - List all users
- GET `/admin/users/{id}` - Get user details
- PUT `/admin/users/{id}` - Update user
- POST `/admin/rooms` - Create room
- PUT `/admin/rooms/{id}` - Update room
- GET `/admin/rooms` - List all rooms (including inactive)
- GET `/admin/bookings` - List all bookings with user details
