@echo off
echo ===== ChatBot Application Setup and Run Script =====
echo.

set VENV_PYTHON=C:\Users\Playdata\web_server\django_venv\Scripts\python.exe
set VENV_PIP=C:\Users\Playdata\web_server\django_venv\Scripts\pip.exe

echo Using Python:
"%VENV_PYTHON%" --version
echo.

echo 1. Installing Python dependencies...
echo.

echo Installing root dependencies...
"%VENV_PIP%" install -r requirements.txt
echo.

echo 2. Setting up Django database...
cd django_webapp
"%VENV_PYTHON%" manage.py makemigrations chat
"%VENV_PYTHON%" manage.py migrate
cd ..
echo.

echo 3. Starting applications...
echo.

echo Starting FastAPI service in background...
start cmd /k "cd /d %~dp0fastapi_langchain && ""%VENV_PYTHON%"" -m uvicorn main:app --reload --port 8001"
timeout /t 3 > nul

echo Starting Django webapp...
start cmd /k "cd /d %~dp0django_webapp && ""%VENV_PYTHON%"" manage.py runserver 8000"

echo.
echo ===== Setup Complete! =====
echo.
echo Applications are running:
echo - Django Web App: http://localhost:8000
echo - FastAPI Service: http://localhost:8001
echo - FastAPI Docs: http://localhost:8001/docs
echo.
echo Make sure to set your OPENAI_API_KEY in fastapi_langchain/.env file!
echo.
pause