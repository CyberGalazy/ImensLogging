@echo off
REM Comprehensive server diagnosis
REM Run this on the laptop where server should be running

echo.
echo ========================================
echo Server Diagnosis
echo ========================================
echo.

REM 1. Check if server process is running
echo [1/5] Checking for server process...
tasklist | findstr /i "pc_logging_server python server.py"
if errorlevel 1 (
    echo   [FAIL] Server process NOT found
    echo   → Server is not running!
) else (
    echo   [OK] Server process found
)

echo.
REM 2. Check if port 8080 is listening
echo [2/5] Checking if port 8080 is listening...
netstat -an | findstr ":8080" | findstr "LISTENING"
if errorlevel 1 (
    echo   [FAIL] Port 8080 is NOT listening
    echo   → Server may have failed to start
) else (
    echo   [OK] Port 8080 is listening
    netstat -an | findstr ":8080" | findstr "LISTENING"
)

echo.
REM 3. Check firewall rules
echo [3/5] Checking firewall rules for port 8080...
netsh advfirewall firewall show rule name=all | findstr /i /c:"8080" /c:"PC Logging"
if errorlevel 1 (
    echo   [FAIL] No firewall rule found for port 8080
) else (
    echo   [OK] Firewall rule(s) found:
    netsh advfirewall firewall show rule name=all | findstr /i /c:"8080" /c:"PC Logging"
)

echo.
REM 4. Check Windows Firewall status
echo [4/5] Checking Windows Firewall status...
netsh advfirewall show allprofiles state
echo.

REM 5. Test local connection
echo [5/5] Testing local connection to server...
curl -s http://localhost:8080/status 2>nul
if errorlevel 1 (
    echo   [FAIL] Cannot connect locally
    echo   → Server may not be responding
) else (
    echo   [OK] Server responds locally
    curl -s http://localhost:8080/status
)

echo.
echo ========================================
echo Recommendations:
echo ========================================
echo.
echo If server not running:
echo   1. Start server: start_server_standalone.bat
echo   2. Check for errors in server window
echo.
echo If port not listening:
echo   1. Check if another program uses port 8080
echo   2. Try different port: python server.py 0.0.0.0 9000
echo.
echo If firewall rule missing:
echo   1. Run as Admin: add_firewall_rule.bat
echo   2. Or add manually in Windows Firewall
echo.
echo If firewall is blocking:
echo   1. Temporarily disable firewall to test
echo   2. Check antivirus firewall settings
echo.
echo ========================================
pause

