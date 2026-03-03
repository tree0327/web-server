#!/bin/bash

echo "===== ChatBot Application Setup and Run Script ====="
echo

echo "1. Installing Python dependencies..."
echo

echo "Installing Django webapp dependencies..."
cd django_webapp
pip install -r requirements.txt
echo

echo "Installing FastAPI LangChain dependencies..."
cd ../fastapi_langchain  
pip install -r requirements.txt
cd ..
echo

echo "2. Setting up Django database..."
cd django_webapp
python manage.py makemigrations chat
python manage.py migrate
echo

echo "3. Starting applications..."
echo

echo "Starting FastAPI service in background..."
cd fastapi_langchain
uvicorn main:app --reload --port 8001 &
FASTAPI_PID=$!
cd ..

echo "Waiting for FastAPI to start..."
sleep 3

echo "Starting Django webapp..."
cd django_webapp
python manage.py runserver 8000 &
DJANGO_PID=$!
cd ..

echo
echo "===== Setup Complete! ====="
echo
echo "Applications are running:"
echo "- Django Web App: http://localhost:8000"
echo "- FastAPI Service: http://localhost:8001"
echo "- FastAPI Docs: http://localhost:8001/docs"
echo
echo "Make sure to set your OPENAI_API_KEY in fastapi_langchain/.env file!"
echo
echo "To stop the applications, run: kill $FASTAPI_PID $DJANGO_PID"
echo

# Wait for user input
read -p "Press Enter to stop the applications..."

# Kill background processes
kill $FASTAPI_PID $DJANGO_PID 2>/dev/null
echo "Applications stopped." 