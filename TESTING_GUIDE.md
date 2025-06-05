# Drum School Scheduling Application - Testing Guide

## Application Overview
A full-stack drum school scheduling application with FastAPI backend, React frontend, and role-based access control.

## Running the Application

### Prerequisites
- Python 3.8+
- Node.js 14+
- VS Code (recommended)

### Starting the Application
1. **Backend Server**: Use VS Code task "Start Backend Server" or run:
   ```bash
   cd backend
   source venv/Scripts/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Server**: Use VS Code task "Start Frontend Server" or run:
   ```bash
   cd frontend
   npm start
   ```

### URLs
- **Frontend Application**: http://localhost:3000
- **Backend API Documentation**: http://localhost:8000/docs
- **Backend Health Check**: http://localhost:8000/health

## Testing Features

### 1. Admin Access
- **Email**: admin@drumschool.com
- **Password**: admin123
- **Capabilities**:
  - View all users and their personal information
  - View all bookings across all users
  - Manage rooms and settings
  - Full administrative control

### 2. User Registration & Authentication
- Navigate to the registration page
- Create a new user account
- Log in with the new credentials
- Test JWT token-based authentication

### 3. Room Booking System
- View available practice rooms
- Book time slots (conflict prevention is implemented)
- View your personal bookings
- Test booking validation and constraints

### 4. Sample Rooms
The application creates sample rooms on startup:
- **Practice Room 1**: Acoustic drum kit
- **Practice Room 2**: Electronic drum setup
- **Recording Studio**: Professional recording equipment

### 5. Role-Based Access Control
- Regular users can only see their own bookings
- Admins can see all users and bookings with personal information
- Test different permission levels

## API Endpoints Testing

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - User login
- GET `/auth/me` - Get current user info

### Rooms
- GET `/rooms/` - List all rooms
- GET `/rooms/{id}` - Get specific room details

### Bookings
- GET `/bookings/` - Get user's bookings
- POST `/bookings/` - Create new booking
- PUT `/bookings/{id}` - Update booking
- DELETE `/bookings/{id}` - Cancel booking

### Admin (Requires admin role)
- GET `/admin/users` - List all users
- GET `/admin/bookings` - List all bookings
- GET `/admin/users/{id}` - Get user details

## Database Features
- **PostgreSQL** database with SQLAlchemy ORM
- **Automatic table creation** on startup
- **Sample data initialization** (admin user and rooms)
- **Relationship management** between users, rooms, and bookings

## Security Features
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- CORS configuration for frontend integration
- Protected routes and API endpoints

## UI/UX Features
- Modern React interface with Tailwind CSS
- Responsive design
- Authentication context management
- Protected routes
- Admin panel with enhanced permissions
- Booking calendar interface
- User-friendly navigation

## Test Scenarios

### Scenario 1: New User Journey
1. Register a new account
2. Log in
3. Browse available rooms
4. Make a booking
5. View your bookings

### Scenario 2: Admin Management
1. Log in as admin
2. View all users
3. View all bookings
4. Access user personal information

### Scenario 3: Booking Conflicts
1. Try to book the same room at the same time
2. Verify conflict prevention works
3. Test booking modification

### Scenario 4: Authentication
1. Try accessing protected pages without login
2. Test login/logout functionality
3. Verify JWT token handling

## Error Handling
- Form validation on frontend
- API error responses
- Authentication failures
- Booking conflicts
- Network error handling

## Development Notes
- Hot reload enabled for both frontend and backend
- Environment variables configured
- Docker support available
- Comprehensive API documentation
- Code follows Python and JavaScript best practices
