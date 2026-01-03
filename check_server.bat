@echo off
REM Check if the server is running and accessible
REM Run this on the laptop where the server should be running

echo.
echo ========================================
echo Server Status Check
echo ========================================
echo.

REM Check if port 8080 is listening
echo [1/2] Checking if port 8080 is listening...
netstat -an | findstr ":8080" | findstr "LISTENING"
if errorlevel 1 (
    echo   [FAIL] Port 8080 is NOT listening
    echo   → Server is not running!
    echo   → Start server with: start_server_standalone.bat
) else (
    echo   [OK] Port 8080 is listening
    echo   → Server appears to be running
)

echo.
echo [2/2] Checking firewall rules for port 8080...
netsh advfirewall firewall show rule name=all | findstr /i "8080"
if errorlevel 1 (
    echo   [WARNING] No firewall rule found for port 8080
    echo   → Firewall may be blocking connections
    echo.
    echo   To add firewall rule, run as Administrator:
    echo   netsh advfirewall firewall add rule name="PC Logging Server" dir=in action=allow protocol=TCP localport=8080
) else (
    echo   [OK] Firewall rule found
)

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. If server not running: Start it now
echo 2. If no firewall rule: Add it (see above)
echo 3. Test from client PC: test_connection.bat
echo ========================================
echo.
pause

