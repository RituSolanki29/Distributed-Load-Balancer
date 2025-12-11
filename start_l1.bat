@echo off
color 0A
echo ========================================
echo    LAPTOP 1 - MAIN CONTROLLER
echo ========================================
echo.
echo Starting services...
echo.

REM Create logs directory
if not exist logs mkdir logs

REM Start ServerA (Video Server)
echo [1/3] Starting ServerA (Video Server)...
start "ServerA-Video" cmd /k "color 0C && python backend_server.py ServerA 5001 video"
timeout /t 3 /nobreak >nul

REM Start Load Balancer
echo [2/3] Starting Load Balancer...
start "LoadBalancer" cmd /k "color 0E && python load_balancer_distributed.py"
timeout /t 3 /nobreak >nul

REM Start Dashboard
echo [3/3] Starting Dashboard...
start "Dashboard" cmd /k "color 0B && python dashboard.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo    ALL SERVICES STARTED!
echo ========================================
echo.
echo Your IP Address:
ipconfig | findstr /C:"IPv4 Address"
echo.
echo Access Points:
echo   Dashboard (local):   http://localhost:9000
echo   Dashboard (network): http://YOUR-IP:9000
echo   Load Balancer:       http://YOUR-IP:8080
echo.
echo ========================================
echo Keep this window open
echo Press Ctrl+C to stop all services
echo ========================================
pause