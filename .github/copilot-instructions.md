<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Drum School Scheduling Application

This is a full-stack application for scheduling practice sessions in a drum school with the following architecture:

## Backend (FastAPI + SQLAlchemy)

- Python FastAPI framework
- SQLAlchemy ORM with PostgreSQL
- JWT authentication for role-based access control
- RESTful API design
- Admin-only access to personal user information

## Frontend (React)

- Modern React application with hooks
- Calendar interface for booking slots
- Role-based UI components
- Integration with backend API

## Key Features

- User registration and authentication
- Time slot booking system with conflict prevention
- Admin panel for reservation management
- Docker containerization
- API documentation with Swagger/OpenAPI

## Development Guidelines

- Follow REST API conventions
- Implement proper error handling
- Use environment variables for configuration
- Maintain separation between user and admin interfaces
- Ensure data privacy compliance
