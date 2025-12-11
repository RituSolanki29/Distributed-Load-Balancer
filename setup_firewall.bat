@echo off
echo ========================================
echo  FIREWALL CONFIGURATION
echo ========================================
echo.
echo This script will allow incoming connections
echo for the Load Balancer system.
echo.
echo IMPORTANT: Run as Administrator!
echo.
pause

echo.
echo Configuring Windows Firewall...
echo.

REM Allow Load Balancer port
netsh advfirewall firewall add rule name="Load Balancer Port 8080" dir=in action=allow protocol=TCP localport=8080
echo [OK] Port 8080 (Load Balancer) allowed

REM Allow Dashboard port
netsh advfirewall firewall add rule name="Dashboard Port 9000" dir=in action=allow protocol=TCP localport=9000
echo [OK] Port 9000 (Dashboard) allowed

REM Allow Backend Server ports
netsh advfirewall firewall add rule name="Backend Servers 5001-5003" dir=in action=allow protocol=TCP localport=5001-5003
echo [OK] Ports 5001-5003 (Backend Servers) allowed

echo.
echo ========================================
echo  FIREWALL CONFIGURED SUCCESSFULLY!
echo ========================================
echo.
echo You can now communicate between laptops.
echo.
pause