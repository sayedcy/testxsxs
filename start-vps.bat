@echo off
echo Starting Security Scanner on VPS (37.60.241.19)...
echo.

echo Starting Backend Server on 0.0.0.0:8000...
start "Backend Server" cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server on 0.0.0.0:5173...
cd frontend
if not exist .env (
    echo VITE_API_URL=http://37.60.241.19:8000 > .env
)
cd ..
start "Frontend Server" cmd /k "cd frontend && npm run dev -- --host 0.0.0.0"

echo.
echo Servers started!
echo Backend: http://37.60.241.19:8000
echo Frontend: http://37.60.241.19:5173
echo.
pause

