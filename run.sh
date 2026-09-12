#!/bin/bash

set -e

echo "🚀 Starting YouTube Lecture Summarizer..."

# Check if .env files exist
if [ ! -f backend/.env ]; then
    echo "⚠️  backend/.env not found. Creating from .env.example..."
    cp backend/.env.example backend/.env
    echo "✏️  Please edit backend/.env and set ANTHROPIC_API_KEY"
fi

if [ ! -f frontend/.env ]; then
    echo "⚠️  frontend/.env not found. Creating from .env.example..."
    cp frontend/.env.example frontend/.env
fi

# Install dependencies if needed
if [ ! -d "backend/venv" ]; then
    echo "📦 Setting up backend environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

sleep 2

# Start frontend
echo "⚡ Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Services started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
