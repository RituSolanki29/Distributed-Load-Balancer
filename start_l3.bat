@echo off
color 0D
echo ========================================
echo    LAPTOP 3 - ServerC
echo ========================================
echo.
echo Starting services...
echo.

REM Start ServerC (Image Server)
echo [1/1] Starting ServerC (Image Server)...
start "ServerC-Image" cmd /k "color 0E && python backend_server.py ServerC 5003 image"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo    ServerC STARTED!
echo ========================================
echo.
echo Your IP Address:
ipconfig | findstr /C:"IPv4 Address"
echo.
echo Server Running:
echo   ServerC (Image): http://YOUR-IP:5003
echo.
echo ========================================
echo Keep this window open
echo ========================================
echo.
echo Press any key to continue...
pause