#!/bin/bash

# Gargeyi's Kitchen - AWS Deployment Script
# This script sets up and launches both the backend (FastAPI) and frontend (Streamlit).

echo "🚀 Starting AWS Deployment Setup..."

# 1. Check for Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Check for .env file and load it
if [ -f .env ]; then
    echo "🔑 Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

source venv/bin/activate

# 3. Install/Update Dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Check for GROQ_API_KEYS
if [ -z "$GROQ_API_KEYS" ]; then
    echo "⚠️  WARNING: GROQ_API_KEYS environment variable is not set."
    echo "Please set it using: export GROQ_API_KEYS='key1,key2,key3,key4,key5'"
    echo "Or add it to your .env file."
fi

# 5. Kill existing processes on ports 8002 and 8501
echo "🧹 Cleaning up existing processes..."
fuser -k 8002/tcp 2>/dev/null
pkill -f uvicorn 2>/dev/null
pkill -f streamlit 2>/dev/null
sleep 2

# 5. Start Backend (FastAPI)
echo "🔥 Starting Backend on port 8002..."
nohup python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8002 > backend.log 2>&1 &
echo "✅ Backend started in background (logs in backend.log)"

# 6. Start Frontend (Streamlit)
echo "🍳 Starting Frontend on port 8501..."
# Streamlit will use its default port 8501
nohup streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 > frontend.log 2>&1 &
echo "✅ Frontend started in background (logs in frontend.log)"

echo "------------------------------------------------------"
echo "✨ Deployment Complete!"
echo "Access the app at: http://your-aws-public-ip:8501"
echo "Backend (Internal): http://localhost:8002"
echo "------------------------------------------------------"
echo "To stop the servers, run: fuser -k 8002/tcp 8501/tcp"
