# Drum School Application - Troubleshooting Guide

## Manual Start Instructions

### Option 1: Manual Backend Start (Recommended)

1. **Open Command Prompt or Bash Terminal**
2. **Navigate to backend directory:**
   ```bash
   cd "d:/Repositórios/projeto-pessoal/backend"
   ```
3. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # For bash
   # OR
   venv\Scripts\activate.bat     # For cmd
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 2: Manual Frontend Start

1. **Open another terminal**
2. **Navigate to frontend directory:**
   ```bash
   cd "d:/Repositórios/projeto-pessoal/frontend"
   ```
3. **Install dependencies:**
   ```bash
   npm install
   ```
4. **Start the frontend server:**
   ```bash
   npm start
   ```

### Option 3: Docker (Easiest)

1. **Make sure Docker is running**
2. **Navigate to project root:**
   ```bash
   cd "d:/Repositórios/projeto-pessoal"
   ```
3. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

## Common Issues and Solutions

### Issue 1: "Connection Refused" Error

- **Cause**: Servers are not actually running
- **Solution**: Check if ports 8000 and 3000 are free and servers are started

### Issue 2: Python/Node.js Not Found

- **Cause**: Python or Node.js not installed or not in PATH
- **Solution**: Install Python 3.8+ and Node.js 14+ and add to PATH

### Issue 3: Dependencies Not Installing

- **Backend**: Make sure you're in the virtual environment
- **Frontend**: Make sure npm is installed and updated

### Issue 4: Database Errors

- **SQLite**: The app uses SQLite by default, no setup needed
- **PostgreSQL**: Use Docker Compose for PostgreSQL setup

## Verification Steps

1. **Check Backend is running:**

   - Open browser to http://localhost:8000
   - Should see welcome message
   - Check http://localhost:8000/docs for API documentation

2. **Check Frontend is running:**

   - Open browser to http://localhost:3000
   - Should see the login page

3. **Test API connection:**
   - Go to http://localhost:8000/health
   - Should return {"status": "healthy"}

## Default Admin Credentials

- **Email**: admin@drumschool.com
- **Password**: admin123

## Port Information

- **Backend API**: http://localhost:8000
- **Frontend App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## If Nothing Works

1. Try restarting your computer
2. Check Windows Firewall settings
3. Try different ports (8001, 3001)
4. Use Docker approach instead of manual setup

## Docker Alternative Commands

```bash
# Start only backend
docker build -t drumschool-backend ./backend
docker run -p 8000:8000 drumschool-backend

# Start only frontend
docker build -t drumschool-frontend ./frontend
docker run -p 3000:3000 drumschool-frontend
```
