@echo off
echo Starting Drum School Application...

echo.
echo Starting Backend Server...
cd /d "d:\Repositórios\projeto-pessoal\backend"
call venv\Scripts\activate.bat
pip install -r requirements.txt
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Frontend Server...
cd /d "d:\Repositórios\projeto-pessoal\frontend"
npm install
start "Frontend Server" cmd /k "npm start"

echo.
echo Both servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo API Documentation at: http://localhost:8000/docs

pause
