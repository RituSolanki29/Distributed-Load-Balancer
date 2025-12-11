@echo off
color 0B
echo ========================================
echo    LAPTOP 2 - ServerB + Test Client
echo ========================================
echo.
echo Starting services...
echo.

REM Start ServerB (API Server)
echo [1/1] Starting ServerB (API Server)...
start "ServerB-API" cmd /k "color 0A && python backend_server.py ServerB 5002 api"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo    ServerB STARTED!
echo ========================================
echo.
echo Your IP Address:
ipconfig | findstr /C:"IPv4 Address"
echo.
echo Server Running:
echo   ServerB (API): http://YOUR-IP:5002
echo.
echo To run test client:
echo   python test_distributed.py
echo.
echo ========================================
echo Keep this window open
echo ========================================
echo.
echo Press any key to continue...
pause