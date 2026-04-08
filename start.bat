@echo off
echo Starting Quantum AI Chef...

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Start backend in new terminal
start "Backend" cmd /k "cd backend && uvicorn main:app --reload --port 8001"

:: Wait 3 seconds for backend to start
timeout /t 3 /nobreak

:: Start frontend in new terminal
start "Frontend" cmd /k "cd frontend && streamlit run app.py"

echo.
echo App is starting...
echo Backend: http://localhost:8001
echo Frontend: http://localhost:8501
echo.
pause