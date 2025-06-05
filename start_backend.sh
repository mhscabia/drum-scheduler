#!/bin/bash

# Navigate to backend directory
cd "d:/Repositórios/projeto-pessoal/backend"

# Activate virtual environment
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
