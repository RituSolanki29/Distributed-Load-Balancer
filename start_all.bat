@echo off
echo ========================================
echo Starting Load Balancer Project
echo ========================================
echo.

REM Start backend servers
echo Starting Backend Servers...
start "ServerA-Video" cmd /k python backend_server.py ServerA 5001 video
timeout /t 2 /nobreak >nul

start "ServerB-API" cmd /k python backend_server.py ServerB 5002 api
timeout /t 2 /nobreak >nul

start "ServerC-Image" cmd /k python backend_server.py ServerC 5003 image
timeout /t 3 /nobreak >nul

REM Start load balancer
echo Starting Load Balancer...
start "LoadBalancer" cmd /k python load_balancer.py
timeout /t 3 /nobreak >nul

REM Start dashboard
echo Starting Dashboard...
start "Dashboard" cmd /k python dashboard.py
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All components started!
echo ========================================
echo.
echo Open in browser: http://localhost:9000
echo.
echo Press any key to exit (services will keep running in separate windows)
pause