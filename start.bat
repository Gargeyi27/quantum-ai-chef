@echo off
echo ========================================
echo    🍳 Quantum AI Chef - Starting Up...
echo ========================================

cd /d C:\Users\Gargeyi\Downloads\Quantum_AI_Chef

set GROQ_API_KEY=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

echo.
echo Starting Backend (FastAPI + Quantum Engine)...
start "Quantum AI Chef - Backend" cmd /k ".venv\Scripts\python -B -m uvicorn backend.main:app --port 8000"

echo Waiting for backend to start...
timeout /t 4 /nobreak > nul

echo.
echo Starting Frontend (Streamlit)...
start "Quantum AI Chef - Frontend" cmd /k ".venv\Scripts\python -m streamlit run frontend/app.py"

echo Waiting for frontend to start...
timeout /t 4 /nobreak > nul

echo.
echo ========================================
echo  App is starting! Opening browser...
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:8501
echo ========================================

start http://localhost:8501

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the app.
pause