@echo off
echo.
echo ========================================
echo Server Status Check
echo ========================================
echo.

echo [1] Checking if port 8080 is listening...
netstat -an | findstr ":8080"
if errorlevel 1 (
    echo   FAIL: Port 8080 is NOT listening
    echo   Server is probably not running!
) else (
    echo   OK: Port 8080 is listening
)

echo.
echo [2] Checking firewall rules...
netsh advfirewall firewall show rule name=all | findstr "8080"
if errorlevel 1 (
    echo   FAIL: No firewall rule for port 8080
) else (
    echo   OK: Firewall rule found
)

echo.
echo [3] Testing local connection...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080/status' -TimeoutSec 2 -UseBasicParsing; Write-Host '  OK: Server responds -' $response.Content } catch { Write-Host '  FAIL: Cannot connect - Server not responding' }"

echo.
echo ========================================
echo What to do:
echo ========================================
echo.
echo If port not listening:
echo   1. Make sure server window is open
echo   2. Start server: start_server_standalone.bat
echo.
echo If no firewall rule:
echo   1. Run as Admin: add_firewall_rule.bat
echo   2. Or manually add rule in Windows Firewall
echo.
echo ========================================
pause

