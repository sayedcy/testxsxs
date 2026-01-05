#!/bin/bash

echo "Starting Security Scanner on VPS (37.60.241.19)..."
echo ""

# Set API URL for frontend
export VITE_API_URL=http://37.60.241.19:8000

echo "Starting Backend Server on 0.0.0.0:8000..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting Frontend Server on 0.0.0.0:5173..."
cd frontend
# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "VITE_API_URL=http://37.60.241.19:8000" > .env
fi
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
cd ..

echo ""
echo "Servers started!"
echo "Backend: http://37.60.241.19:8000"
echo "Frontend: http://37.60.241.19:5173"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait

