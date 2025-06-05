# Drum School Scheduling Application

A full-stack web application for scheduling practice sessions in a drum school. Students can book time slots for practice rooms, and administrators can manage users, rooms, and view all bookings with user details.

## 🆕 Latest Updates

- **Timezone Handling Fix**: Improved validation for time slot bookings to properly handle timezones
- **Portuguese Translation**: Error messages now displayed in Portuguese
- **Booking Buffer**: Added 15-minute buffer for scheduling to prevent last-minute bookings

## 🚀 Features

- **User Authentication**: JWT-based authentication with role-based access control
- **Room Booking**: Interactive calendar interface for booking practice sessions
- **Conflict Prevention**: Automatic prevention of double bookings
- **Admin Panel**: Comprehensive admin interface for managing users, rooms, and bookings
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Updates**: Live availability updates

## 🏗️ Architecture

### Backend (FastAPI)

- **Framework**: FastAPI with automatic OpenAPI documentation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with role-based access control
- **API**: RESTful API design with comprehensive error handling

### Frontend (React)

- **Framework**: React 18 with hooks
- **Styling**: Tailwind CSS for modern UI
- **State Management**: Context API for authentication
- **Routing**: React Router for navigation
- **Icons**: Lucide React for beautiful icons

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL, JWT
- **Frontend**: React, Tailwind CSS, Axios, React Router
- **Deployment**: Docker, Docker Compose
- **Database**: PostgreSQL (production), SQLite (development)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional)

### Option 1: Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd drum-school-scheduling
```

2. Start with Docker Compose:

```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy environment file:

```bash
cp .env.example .env
```

5. Run the server:

```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Install Tailwind CSS:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

4. Start the development server:

```bash
npm start
```

## 🔑 Default Admin Account

- **Email**: admin@drumschool.com
- **Password**: admin123

**⚠️ Important**: Change the admin password in production!

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Key Features

### For Students

- Register and login securely
- Browse available practice rooms
- View real-time availability calendar
- Book practice sessions
- Manage personal bookings
- Cancel upcoming bookings

### For Administrators

- Access all user information and contact details
- View all bookings with user details
- Manage practice rooms (create, edit, deactivate)
- Monitor system usage and statistics

## 🔒 Security

- JWT token-based authentication
- Role-based access control (Admin/User)
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- Admin-only access to personal user information

## 🏢 Room Management

- Multiple practice rooms with different equipment
- Configurable capacity and equipment lists
- Room availability scheduling
- Equipment tracking and descriptions

## 📅 Booking System

- Hourly time slot booking
- Conflict detection and prevention
- Business hours enforcement (9 AM - 9 PM)
- Booking status management (confirmed, cancelled, completed)
- Notes and additional information support

## 🐳 Docker Deployment

The application includes complete Docker configuration:

- **Backend**: Python FastAPI container
- **Frontend**: Node.js React container
- **Database**: PostgreSQL container
- **Orchestration**: Docker Compose for easy deployment

## 🔧 Environment Configuration

### Backend (.env)

```env
DATABASE_URL=postgresql://username:password@localhost/drumschool_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_EMAIL=admin@drumschool.com
ADMIN_PASSWORD=admin123
```

### Frontend

```env
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📁 Project Structure

```
drum-school-scheduling/
├── backend/
│   ├── app/
│   │   ├── routers/          # API route handlers
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── auth.py          # Authentication logic
│   │   ├── crud.py          # Database operations
│   │   ├── database.py      # Database configuration
│   │   ├── config.py        # App configuration
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── services/       # API services
│   │   └── App.js          # Main app component
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please check the API documentation at `/docs` or create an issue in the repository.
